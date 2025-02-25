from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Reminder
from session.models import Medications
from session.serializers import MedicationsSerializer



class SetReminder(APIView):
    def post(self ,request, id):

        try:
            medication = Medications.objects.get(pk=id)

        except Medications.DoesNotExist:
            return Response({'error':'medication not found'}, status=status.HTTP_400_BAD_REQUEST)
        

        reminder = Reminder.objects.create(
            medication = medication,
            user = request.user,
            email = request.data.get('email'),
            time = request.data.get('time'),
            phone = request.data.get('phoneNumber'),
            message = f"Reminder created for {medication.name}"
        )


        medication.has_reminder = True
        medication.save()

        serializer = MedicationsSerializer(medication)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class DeleteReminder(APIView):
    def post(self, request,  id):

        try:
            medication = Medications.objects.get(pk=id)

        except Medications.DoesNotExist:
            return Response({'error':'medication not found'}, status=status.HTTP_400_BAD_REQUEST)
        

        reminder = Reminder.objects.get(medication=medication)
        reminder.delete()

        medication.has_reminder = False
        medication.save()


       

        serializer = MedicationsSerializer(medication)

        return Response(serializer.data, status=status.HTTP_200_OK)




