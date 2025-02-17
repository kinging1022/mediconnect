from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields =('id', 'body', 'type_of_notification', 'created_for', 'created_by', 'created_at','created_at_formatted','is_read' )