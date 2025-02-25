
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import DoctorSession, DoctorSessionMessage , Medications
from appointment.models import Appointment
from notification.utils import create_notification
from notification.models import Notification
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import SessionDetailSerializer, SessionMessageSerializer




class GetOrCreateSession(APIView):

    def post(self,request):

        id = request.data.get('appointmentId')

        try:
            appointment = Appointment.objects.get(pk=id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment with the given ID does not exist."}, status=status.HTTP_404_NOT_FOUND)



        with transaction.atomic():
            doctor = appointment.created_for
            patient = appointment.created_by


            session = DoctorSession.objects.filter(users=doctor).filter(users=patient).distinct()

            if session.exists():
                session = session.first()
                session.status = session.STARTED

                session.save()

            
            else:
                session = DoctorSession.objects.create(appointment=appointment)
                session.users.add(patient, doctor)


            notiication = create_notification(doctor,patient,Notification.SESSION_START)


            serializer = SessionDetailSerializer(session)

            return Response(serializer.data,status=status.HTTP_200_OK)
        



class GetActiveSession(APIView):

    def get(self, request):
        try:
            session = DoctorSession.objects.get(users=request.user,status=DoctorSession.STARTED)

        except DoctorSession.DoesNotExist:
            return Response({'message':'No active session'}, status=status.HTTP_204_NO_CONTENT)


        serializer = SessionDetailSerializer(session)

        return Response(serializer.data,status=status.HTTP_200_OK)
    



class GetSessionMessages(APIView):

    def get(self,request):

        session_id = request.GET.get('sessionId')

        try:


            messages = DoctorSessionMessage.objects.filter(doctor_session=session_id)

            serializer = SessionMessageSerializer(messages, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except DoctorSession.DoesNotExist:
            return Response({'error':'Session does not exist'}, status=status.HTTP_400_BAD_REQUEST)



class AddMedications(APIView):

    def post(self, request, id):
        try:
            doctor_session = DoctorSession.objects.get(pk=id)

        except DoctorSession.DoesNotExist:
            return Response({'error': "Doctor session not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        medications_data = request.data
        if not medications_data or not isinstance(medications_data, list):
            return Response({"error": "Invalid or empty data format. Expected a non-empty array of objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        users = doctor_session.users

        try:
            patient = users.exclude(pk=request.user.id).filter(role='patient').first()

        except Exception as e:
            return Response({'error': f"Error identifying patient: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        if not patient:
            return Response({'error': 'Unable to identify patient'}, status=status.HTTP_400_BAD_REQUEST)
        

        medications = [
            Medications(
                doctor_session = doctor_session,
                name = data.get('name'),
                weight = data.get('weight'),
                dosage = data.get('dosage'),
                created_by = request.user,
                created_for = patient


            )
            for data in medications_data if all([data.get('name'),data.get('weight'), data.get('dosage')])
        ]

        if len(medications) != len(medications_data):
            return Response({"error": "Missing fields in some prescriptions"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            Medications.objects.bulk_create(medications)

        except Exception as e:
            return Response({'error': f'Failed to add medications: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        message = f'{len(medications)} medications were added to this session' if len(medications) > 1 else f'{len(medications)} medication was added to this session' 

        return Response({'message': message }  , status=status.HTTP_201_CREATED)



class AddFollowup(APIView):
    def post(self, request, id):

        try:
            doctor_session = DoctorSession.objects.get(pk=id)

        except DoctorSession.DoesNotExist:
            return Response({'error': "Doctor session not found"}, status=status.HTTP_404_NOT_FOUND)
        

        appointment = doctor_session.appointment

        if not appointment:
            return Response({'error':'Appoitment not found'}, status=status.HTTP_400_BAD_REQUEST)
        

        appointment.follow_up_allowed = True

        appointment.save()

        return Response({'message':f'Dr {appointment.created_for.first_name} added follow up to this appointment , it will be valid for 30 days'}, status=status.HTTP_201_CREATED)
        



class SessionHistory(APIView):
    def get(self,request):
        sessions = DoctorSession.objects.filter(users=request.user, status=DoctorSession.ENDED)

        serializer = SessionDetailSerializer(sessions, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    


class ViewSession(APIView):
    def get(self,request):
        
        session_id = request.GET.get('sessionId')

        try:
            doctor_session = DoctorSession.objects.get(pk=session_id)

        except DoctorSession.DoesNotExist:
            return Response({'error':'session not found'},status=status.HTTP_400_BAD_REQUEST)
    
        serializer = SessionDetailSerializer(doctor_session)

        return Response(serializer.data, status=status.HTTP_200_OK)




class UploadFile(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, session_id):
        print(f"Upload request received for session {session_id}")
        print(f"Request data: {request.data}")
        print(f"Request FILES: {request.FILES}")
        
        try:
            session = DoctorSession.objects.get(id=session_id)
        except DoctorSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)
        
        # Get files from request.FILES
        files = request.FILES
        
        if not files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process each file
        processed_files = []
        for file_key in files:
            file = files[file_key]
            
            # Determine message type based on file mime type
            mime_type = file.content_type
            print(f"Processing file: {file.name}, type: {mime_type}")
            
            if mime_type.startswith('video/'):
                message_type = 'video'
            elif mime_type.startswith('image/'):
                message_type = 'image'
            else:
                print(f"Unsupported file type: {mime_type}")
                continue
            
            # Create message with file
            message = DoctorSessionMessage.objects.create(
                doctor_session=session,
                body=request.data.get('message', ''),
                created_by=request.user,
                type=message_type,
                file=file
            )
            
            serializer = SessionMessageSerializer(message)
            processed_files.append(serializer.data)
            print(f"Created message: {message.id}")
        
        if not processed_files:
            return Response({"error": "No valid files processed"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return all processed files
        response_data = {
            "message": "Files uploaded successfully",
            "files": processed_files
        }
        print(f"Response data: {response_data}")
        return Response(response_data, status=status.HTTP_201_CREATED)