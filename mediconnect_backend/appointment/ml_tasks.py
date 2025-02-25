import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import logging
import numpy as np
import faiss
from celery import shared_task

from sentence_transformers import SentenceTransformer
from .models import Appointment
from account.models import User
from notification.models import Notification
import torch
import gc
import threading
from notification.utils import create_notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import AppointmentSerializer

logger = logging.getLogger(__name__)




# Thread-local storage for model
_thread_local = threading.local()

def get_model():
    """Thread-safe lazy loading of the model"""
    if not hasattr(_thread_local, 'model'):
        try:
            # Explicit CPU device placement
            _thread_local.model = SentenceTransformer(
                "intfloat/multilingual-e5-small",
                device="cpu"
            )
        except Exception as e:
            logger.error(f"Model loading error: {str(e)}")
            raise
    return _thread_local.model

def safe_encode(model, texts, batch_size=1):
    """Safe encoding with explicit memory handling"""
    try:
        with torch.no_grad():
            embeddings = model.encode(
                texts,
                normalize_embeddings=True,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
        return embeddings.astype(np.float32)
    except Exception as e:
        logger.error(f"Encoding error: {str(e)}")
        raise
    finally:
        gc.collect()

def find_best_doctor(symptoms):
    """Find best matching doctor with improved error handling"""
    try:
        doctors = User.objects.filter(role=User.DOCTOR)
        if not doctors:
            return None

        doctor_texts = [f"{doc.speciality}" for doc in doctors]
        
        # Get model instance
        model = get_model()
        
        # Create FAISS index
        doctor_embeddings = safe_encode(model, doctor_texts)
        dimension = doctor_embeddings.shape[1]
        
        # Use CPU index
        index = faiss.IndexFlatL2(dimension)
        index.add(doctor_embeddings)
        
        # Encode query
        query_embedding = safe_encode(model, [symptoms])
        
        # Search
        D, I = index.search(query_embedding, k=1)
        
        if I[0][0] == -1:
            return None
            
        return doctors[int(I[0][0])]
        
    except Exception as e:
        logger.error(f"Doctor matching error: {str(e)}")
        return None
    finally:
        gc.collect()
        torch.cuda.empty_cache()



@shared_task(
    bind=True,
    max_retries=2,
    default_retry_delay=300,
    rate_limit='5/m',
    time_limit=180,
    soft_time_limit=120,
    queue='ml_tasks'  

)
def process_appointments(self, batch_size=3):
    """Process appointments with minimal batch size"""
    try:
        appointments = Appointment.objects.filter(
            status=Appointment.SENT
        )[:batch_size]

        for appointment in appointments:
            try:
                if appointment.created_for:
                    appointment.status = Appointment.PROCESSED
                else:
                    best_doctor = find_best_doctor(appointment.symptoms)
                    if best_doctor:
                        appointment.created_for = best_doctor
                        appointment.status = Appointment.PROCESSED


                    
                appointment.save()
                
                
                serializer = AppointmentSerializer(appointment)
                serialized_data = serializer.data

                channel_layer = get_channel_layer()
                
                async_to_sync(channel_layer.group_send)(
                    f"patient_{appointment.created_by.id}",
                    {"type": "update_appointment", "data": serialized_data}
                )


                async_to_sync(channel_layer.group_send)(
                    f"doctor_{appointment.created_for.id}",
                    {"type": "new_appointment", "data": serialized_data}  
                )


                notification1 = create_notification(appointment.created_for, appointment.created_by,Notification.CONSULTATION)

                notification2 = create_notification(appointment.created_by, appointment.created_for, Notification.CONSULTATION)

                

                
                
            except Exception as e:
                logger.error(f"Appointment processing error: {str(e)}")
                continue
            finally:
                gc.collect()
                

    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise self.retry(exc=e)
