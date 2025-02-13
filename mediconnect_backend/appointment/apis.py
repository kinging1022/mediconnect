from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer



class BookAppointmentOrFollow(APIView):
    def post(self,request):
        appointment_type = request.data.get('type')


        if appointment_type == 'follow-up':
           
            appointments = Appointment.objects.filter(created_by=request.user, follow_up_allowed=True)

            valid_appointments = [appointment for appointment in appointments if appointment.can_book_follow_up()]

            if not valid_appointments:
                return Response({'error':'No follow up appointment'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = AppointmentSerializer(valid_appointments, many=True)
            

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid appointment type'}, status=status.HTTP_400_BAD_REQUEST)

            
            
            

class ConfirmFollowUp(APIView):

    def post(self,request):
        id = request.data.get('id')

        try:
            appointment = Appointment.objects.get(pk=id)
            
            new_appointment = Appointment.objects.create(
                symptoms = f'Follow up for last appointment {appointment.created_at}',
                created_by = request.user,
                created_for = appointment.created_for,
                status = Appointment.SENT
            )
            return Response({'messaage':'Follow appointment created'}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error':'Appoinment not found'})