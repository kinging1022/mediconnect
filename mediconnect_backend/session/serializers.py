from rest_framework import serializers
from .models import  DoctorSession, DoctorSessionMessage, Medications
from account.serializers import UserSerializer
from appointment.serializers import AppointmentSerializer





class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSession
        fields = ('id', 'users', 'status', )
    
    

class SessionMessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = DoctorSessionMessage
        fields = ('id','created_by', 'created_at_formatted','body','type','get_image','get_video',)

      

    



class SessionDetailSerializer(serializers.ModelSerializer):
    messages = SessionMessageSerializer(read_only=True, many=True)
    appointment = AppointmentSerializer(read_only = True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = DoctorSession
        fields = ('id', 'users', 'status',  'messages','appointment')

        
        

   

class MedicationsSerializer(serializers.ModelSerializer):
    doctor_session = SessionDetailSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)

    class Meta:
        model = Medications
        fields = ('id', 'doctor_session','name', 'weight', 'dosage','created_by','created_for','created_at_formatted','has_reminder' )
    
    
