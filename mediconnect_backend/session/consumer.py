import json
import uuid
import asyncio
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from .models import DoctorSession, DoctorSessionMessage
from .serializers import SessionMessageSerializer
from django.core.serializers.json import DjangoJSONEncoder
from account.models import User
from appointment.models import Appointment


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.room_group_name = f"chat_{self.session_id}"

        session = await sync_to_async(DoctorSession.objects.filter)(id=self.session_id)

        if not await sync_to_async(session.exists)():
            await self.close()
            return

        session = await sync_to_async(session.first)()
        user = self.scope["user"]

        # Get list of user IDs in the session
        session_user_ids = await sync_to_async(lambda: list(session.users.values_list('id', flat=True)))()
        
        if user == AnonymousUser() or (user.id not in session_user_ids):
            await self.close()
            return
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        appointment = await sync_to_async(lambda: session.appointment)()

        await sync_to_async(Appointment.objects.filter(id=appointment.id).update)(
            status = Appointment.IN_SESSION
        )


    
    async def encode_json(self, content):
        return json.dumps(content, cls=CustomJSONEncoder)

    
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user = self.scope["user"]
            session = await sync_to_async(DoctorSession.objects.get)(id=self.session_id)

            # Get list of user IDs in the session
            session_user_ids = await sync_to_async(lambda: list(session.users.values_list('id', flat=True)))()
            
            if user.id not in session_user_ids:
                return

            # Check if session is already ended
            if await sync_to_async(lambda: session.status == "ended")():
                await self.send(text_data=await self.encode_json({
                    "type": "error",
                    "message": "This session has already ended"
                }))
                return

            # Handle end session request
            if data.get("type") == "end_session":
                await self.end_session()
                return
            
            # Create and broadcast regular message
            message = await sync_to_async(DoctorSessionMessage.objects.create)(
                doctor_session=session,
                created_by=user,
                body=data["message"],
                type=data["type"]
            )

            serialized_message = await sync_to_async(SessionMessageSerializer)(message)
            serialized_data = await sync_to_async(lambda: serialized_message.data)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "data": serialized_data
                }
            )

        except json.JSONDecodeError:
            await self.send(text_data=await self.encode_json({
                "type": "error",
                "message": "Invalid message format"
            }))
        except Exception as e:
            await self.send(text_data=await self.encode_json({
                "type": "error",
                "message": "An error occurred while processing your message"
            }))

    async def end_session(self):
        try:
            session = await sync_to_async(DoctorSession.objects.get)(id=self.session_id)
            
            # Check if session is already ended
            if await sync_to_async(lambda: session.status == DoctorSession.ENDED)():
                return
            
            # Check if user has permission to end session
            user = self.scope["user"]
            is_doctor = await sync_to_async(lambda: user.role == User.DOCTOR)()
            
            if not is_doctor:
                await self.send(text_data=await self.encode_json({
                    "type": "error",
                    "message": "Only the doctor can end the session"
                }))
                return
            
            
            
            # Update session status
            await sync_to_async(DoctorSession.objects.filter(id=self.session_id).update)(
                status=DoctorSession.ENDED,
            )

            # Create end session notification
            end_message = f"Dr. {user.first_name} ended the session"
            message = await sync_to_async(DoctorSessionMessage.objects.create)(
                doctor_session=session,
                created_by=user,
                body=end_message,
                type='notification'
            )

            serialized_message = await sync_to_async(SessionMessageSerializer)(message)
            serialized_data = await sync_to_async(lambda: serialized_message.data)()

            appointment = await sync_to_async(lambda: session.appointment)()

            await sync_to_async(Appointment.objects.filter(id=appointment.id).update)(
                status = Appointment.DONE
            )

            # Notify all participants
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "session_ended",
                    "data": {
                        "message": serialized_data,
                        "session_status": "ended"
                    }
                }
            )

            # Log successful end session
            print(f"Session {self.session_id} ended successfully by {user.username}")
            
            # Brief delay to ensure message delivery before disconnection
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error ending session: {str(e)}")
            await self.send(text_data=await self.encode_json({
                "type": "error",
                "message": f"Failed to end session: {str(e)}"
            }))

    async def session_ended(self, event):
        """Handle session ended event"""
        await self.send(text_data=await self.encode_json(event))

    async def chat_message(self, event):
        """Handle regular chat messages"""
        await self.send(text_data=await self.encode_json(event))