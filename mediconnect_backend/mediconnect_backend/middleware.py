from datetime import datetime, timezone
import os
import django
import jwt
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from account.models import User
from django.db import close_old_connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

ALGORITHM = "HS256"

@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        print('payload', payload)
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return AnonymousUser()
    except jwt.InvalidTokenError:
        print("Invalid token")
        return AnonymousUser()
    except Exception as e:
        print("Error decoding token:", e)
        return AnonymousUser()

    # Check token expiration
    token_exp = datetime.fromtimestamp(payload['exp'], timezone.utc)
    if token_exp < datetime.now(timezone.utc):
        print("Token has expired")
        return AnonymousUser()

    # Fetch user
    try:
        user = User.objects.get(id=payload['user_id'])
        print('user', user)
        return user
    except User.DoesNotExist:
        print("No user found")
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        # Extract token from query string
        query_string = scope['query_string'].decode()
        try:
            token_key = dict((x.split('=') for x in query_string.split("&"))).get('token', None)
        except ValueError:
            token_key = None

        # Get user from token
        scope['user'] = await get_user(token_key)
        print('User from token:', scope['user'])
        
        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
