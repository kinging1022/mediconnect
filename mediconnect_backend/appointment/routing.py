from django.urls import re_path
from .consumer import AppointmentConsumer

websocket_urlpatterns = [
    re_path(r"ws/appointments/(?P<user_type>\w+)/(?P<user_id>[\w-]+)/$", AppointmentConsumer.as_asgi()),

]