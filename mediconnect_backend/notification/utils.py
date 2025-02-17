from .models import Notification
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .serializers import NotificationSerializer


def create_notification(created_by, created_for, notification_type):
    message = {
        'appointment': 'Your appointment was created succesfully, you will be matched to your doctor soon',
        'consultation_doctor': f'A consultation request was created for {created_by.first_name} {created_by.last_name}',
        'consultation_patient': 'Your appointment request has been processed and your doctor will contact you soon',
        'session_start_patient': f'Dr {created_by.first_name} created a session',
        'session_start_doctor': f'You started a session with {created_by.first_name} {created_by.last_name}',
        'session_stop_patient': f'Your session with Dr {created_by.first_name} has ended',
        'message':f'Dr {created_by.first_name} sent you a message.' if created_by.role == 'doctor' else f'{created_by.first_name} sent you a message'

    }

    role_key = f"{notification_type}_{created_for.role}" if notification_type in ['consultation', 'session_start', 'session_stop'] else notification_type


    body = message.get(role_key, "A new notification was created")


    with transaction.atomic():
        notification = Notification.objects.create(
            created_by = created_by,
            created_for = created_for,
            type_of_notification=notification_type,
            body=body
        )

    
    serialized_data = NotificationSerializer(notification).data
    
    channel_layer = get_channel_layer()

            

    async_to_sync(channel_layer.group_send)(
        f"user_{notification.created_for.id}",
        {"type": "new_notification", "data": serialized_data}  
    )



    return notification