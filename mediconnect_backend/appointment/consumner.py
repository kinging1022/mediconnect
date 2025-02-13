from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import Appointment
from .serializers import AppointmentSerializer
import uuid
from datetime import datetime 




class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


class AppointmentConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    async def encode_json(self, content):
        return json.dumps(content, cls=CustomJSONEncoder)

    async def send_json(self, content, close=False):
        await self.send(text_data=await self.encode_json(content), close=close)

    def filter_queryset(self, queryset, **kwargs):
        user = self.scope['user']
        if user.role == 'doctor':
            return queryset.filter(created_for=user)
        return queryset.filter(created_by=user)

    async def connect(self):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Appointment)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return {
            'data': AppointmentSerializer(instance=instance).data,
            'action': action.value
        }