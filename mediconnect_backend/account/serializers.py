from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from account.models import User



class CustomTokenObtainPairSerrializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError({'detail':'No active account found with the given credentials'})
            

            if not user.is_active:
                raise serializers.ValidationError ({'detail':'Account is inactive, click the link sent to your email to activate your account'})
            

        except User.DoesNotExist:
            raise serializers.ValidationError({'detail':'No active account found with the given credentials'})
       
       
        data =  super().validate(attrs)

        return data
    


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="A user with this email address exists"
        )]
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', "password", "password2")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        read_only_fields = (
            'display_age',
        )

        fields = ('id','first_name','last_name', 'email','gender','role','phone','speciality','display_age','height',
                  'weight','allergies','emergency_contact_name','emergency_contact_number','blood_type','role')



