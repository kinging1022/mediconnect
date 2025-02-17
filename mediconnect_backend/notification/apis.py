from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification





class ReadNotification(APIView):
    
    def post(self, request):
        notification_id = request.data.get('id')
        print(notification_id)


        try:
            notification = Notification.objects.get(pk=notification_id)

            notification.is_read = True
            notification.save()
            return Response({'message','successful'},status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response({'error':'Notification not found'}, status = status.HTTP_400_BAD_REQUEST )





class ReadAllNotifications(APIView):
    
    def post(self, request):
        notifications = Notification.objects.filter(is_read=False,created_for = request.user)


        for notification in notifications:
            notification.is_read = True

            notification.save()

        return Response({'message':'succesful'},status=status.HTTP_200_OK)


        