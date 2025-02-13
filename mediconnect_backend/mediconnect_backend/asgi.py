
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from appointment.routing import websocket_urlpatterns as appointment_websocket_urlpatterns
from .middleware import JwtAuthMiddlewareStack

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediconnect_backend.settings')
django.setup()



  # Import your custom middleware


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            appointment_websocket_urlpatterns 
        )
    ),
})