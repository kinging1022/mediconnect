import json
import uuid
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async
from .models import Notification
from .serializers import NotificationSerializer


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return(str(obj))
        if isinstance(obj,datetime):
            return obj.isoformat()
        return super().default(obj)
    

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        await self.accept()

        await self.channel_layer.group_add(f'user_{self.user_id}',self.channel_name)
        
        await self.send_notifications(user_id = self.user_id)


    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(f'user_{self.user_id}', self.channel_name)



    async def encode_json(self,content):
        return json.dumps(content, cls=CustomJSONEncoder)
    

    async def send_notifications(self, user_id=None):
        
        notifications = await sync_to_async(self.get_notifications)(user_id)

        serialized_notifications = await sync_to_async(self.serialize_notification)(notifications)

        await self.send(text_data=await self.encode_json({"event": "list_notifications", "data":serialized_notifications}))

    
    
        

    def get_notifications(self, user_id):
        if user_id:
            return list(Notification.objects.filter(created_for =user_id).all())
        
        else:
            return []
        

    def serialize_notification(self,notifications):

        return NotificationSerializer(notifications, many=True).data
    


    async def new_notification(self, event):
        await self.send(text_data= await self.encode_json({
            "event": "new_notification",
            "data": event["data"]
        }))
        
