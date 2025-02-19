from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import DoctorSession, DoctorSessionMessage , Medications
from appointment.models import Appointment
from notification.utils import create_notification
from notification.models import Notification
from django.db import transaction
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


            session = DoctorSession.objects.filter(users=doctor).filter(users=doctor).distinct()

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
        