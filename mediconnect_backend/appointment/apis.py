from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from notification.models import Notification
from notification.utils import create_notification



class BookAppointmentOrFollow(APIView):
    def post(self, request):

        user = request.user
    
        check = Appointment.objects.filter(created_by = user).order_by('-created_at').first()

        if check and check.status != Appointment.DONE:

            return Response(
                {'error': 'You cannot create a new appointment until your current appointmemt is completed'}, status=status.HTTP_400_BAD_REQUEST
            )
    
        appointment_type = request.data.get('type')

        if appointment_type == 'follow-up':
            appointments = Appointment.objects.filter(
                created_by=request.user, follow_up_allowed=True
            )

            valid_appointments = [appointment for appointment in appointments if appointment.can_book_follow_up()]

            if not valid_appointments:
                return Response({'error': 'No follow-up appointment available'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = AppointmentSerializer(valid_appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif appointment_type == 'new':
            symptoms = request.data.get('symptoms')

            appointment = Appointment.objects.create(
                created_by=request.user,
                symptoms=symptoms
            )

            serializer = AppointmentSerializer(appointment)
            serialized_data = serializer.data  

            channel_layer = get_channel_layer()

            

            async_to_sync(channel_layer.group_send)(
                f"patient_{appointment.created_by.id}",
                {"type": "new_appointment", "data": serialized_data}  
            )

            # Send notification
            create_notification(appointment.created_by, appointment.created_by, Notification.APPOINTMENT)

            return Response(serialized_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid appointment type'}, status=status.HTTP_400_BAD_REQUEST)

            
            
            

class ConfirmFollowUp(APIView):

    def post(self,request):
        id = request.data.get('id')

        try:
            appointment = Appointment.objects.get(pk=id)
            
            new_appointment = Appointment.objects.create(
                symptoms = f'Follow up for last appointment {appointment.created_at.strftime("%B %d, %Y, %I:%M %p")}',
                created_for = appointment.created_for,
                status = Appointment.SENT
            )
            return Response({'messaage':'Follow appointment created', 'appointment':new_appointment}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error':'Appoinment not found'})
        


class getRecentAppointments(APIView):

    def get(self, request):

        appointments = Appointment.objects.filter(created_for=request.user, status=Appointment.DONE)

        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


