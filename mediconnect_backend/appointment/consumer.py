import json
import uuid
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async
from .models import Appointment
from .serializers import AppointmentSerializer


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class AppointmentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_type = self.scope["url_route"]["kwargs"]["user_type"]
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        await self.accept()

        if self.user_type == "doctor":
            await self.channel_layer.group_add(f"doctor_{self.user_id}", self.channel_name)
            await self.send_appointments(doctor_id=self.user_id)

        elif self.user_type == "patient":
            await self.channel_layer.group_add(f"patient_{self.user_id}", self.channel_name)
            await self.send_appointments(patient_id=self.user_id)

   
    async def disconnect(self, code):
        if self.user_type == "doctor":
            await self.channel_layer.group_discard(f"doctor_{self.user_id}", self.channel_name)
        elif self.user_type == "patient":
            await self.channel_layer.group_discard(f"patient_{self.user_id}", self.channel_name)

    
    async def encode_json(self, content):
        return json.dumps(content, cls=CustomJSONEncoder)

    
    async def send_appointments(self, doctor_id=None, patient_id=None):
        appointments = await sync_to_async(self.get_appointments)(doctor_id, patient_id)
        serialized_appointments = await sync_to_async(self.serialize_appointments)(appointments)

        await self.send(text_data=await self.encode_json({"event": "list_appointments", "data": serialized_appointments}))

    
    
    def get_appointments(self, doctor_id, patient_id):
        if doctor_id:
            return list(Appointment.objects.filter(created_for=doctor_id, status=Appointment.PROCESSED).all())
        elif patient_id:
            return list(Appointment.objects.filter(created_by=patient_id).all())
        return []

    
    def serialize_appointments(self, appointments):
        return AppointmentSerializer(appointments, many=True).data

    
    async def new_appointment(self, event):
        await self.send(text_data=await self.encode_json({"event": "new_appointment", "data": event["data"]}))

    
    async def update_appointment(self, event):
        await self.send(text_data=await self.encode_json({"event": "update_appointment", "data": event["data"]}))
