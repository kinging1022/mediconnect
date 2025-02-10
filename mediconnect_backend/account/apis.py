import jwt
import datetime
from urllib.parse import quote

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from account.models import User
from django.core.exceptions import ValidationError
from .serializers import CustomTokenObtainPairSerrializer,UserCreateSerializer,UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import uuid

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerrializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)


        try:
            serializer.is_valid(raise_exception=True)

        except ValidationError as e:
            return Response(e.detail,status=status.HTTP_400_BAD_REQUEST)
        

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {'message': 'User registration successful. click the activation link sent to your email address to activate your account'},
                    status=status.HTTP_201_CREATED
                )
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        


class SendActivationEmail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)

            pay_load = {
                'user_id': str(user.id),  
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15),
                'iat': datetime.datetime.now(datetime.timezone.utc)
            }

            token = jwt.encode(pay_load, settings.SECRET_KEY, algorithm="HS256")

            # URL encode the token to handle special characters
            encoded_token = quote(token)
            activate_url = f"http://localhost:5173/acount/activate/{encoded_token}"

            send_mail(
                "Mediconnect account activation email",
                f"Click the link to activate your account: {activate_url}",
                "noreply@example.com",
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Activation email sent successfully'})

        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=404)
        


class ActivateEmail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get('token')
        print(f"Received token: {token}")  # Debug print

        if not token:
            return Response({'error':'token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  
            print(f"Decoded payload: {payload}")

            user = User.objects.get(id=uuid.UUID(payload['user_id']))
            print(f"Found user: {user.email}")

            user.is_active = True
            user.save()

            return Response({'message':'Account activation successful'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            print(f"Token expired error: {str(e)}")
            return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as e:
            print(f"Token decode error: {str(e)}")
            return Response({'error': "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist as e:
            print(f"User not found error: {str(e)}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class PasswordEdit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password =request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not check_password(current_password,user.password):
            return Response({'error':'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({"error": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        if  current_password == new_password:
            return Response({'error':'New password cannot be the same as old password'},status=status.HTTP_400_BAD_REQUEST)



        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    

class PasswordResetRequest(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self,request):
        
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)


        except User.DoesNotExist:
            return Response({'error':'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            return Response({'error':'your account is inactive , click the link sent to your email to activate your account'},status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            'user_id': str(user.id),
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.now(datetime.timezone.utc)

        }

        token  = jwt.encode(payload,settings.SECRET_KEY, algorithm="HS256")

        reset_url = f"http://localhost:5173/reset-password/{token}"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_url}",
            "noreply@example.com",
            [email],
            fail_silently=False,
        )

        return Response({'message':'password reset link sent to your email'})

        



class ResetPassword(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not token:
            return Response({'error':'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Decode the token and get the user

            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=["HS256"])

            #Retrieve user using decoded payload

            user = User.objects.get(id=uuid.UUID(payload['user_id']))


            #set new password

            user.set_password(new_password)
            user.save()

            return Response({'message':'Password reset succesful'},status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError:
            return Response({'error': "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)





