from rest_framework import serializers
from .models import Appointment
from account.serializers import UserSerializer



class AppointmentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    created_at_formatted = serializers.CharField(read_only=True)
    follow_up_expiry_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

   
    class Meta:
         model = Appointment

         read_only_fields = ('follow_up_expiry_date','can_book_follow_up')
         
         fields = ('id','symptoms','created_by','created_for','created_at','status','follow_up_allowed','follow_up_expiry_date','can_book_follow_up','created_at_formatted')