from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
import uuid
from datetime import date , datetime


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        if 'is_active' not in extra_fields:
            user.is_active = False
        
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        

        return self.create_user(email, password, **extra_fields)
    


class User(AbstractBaseUser,PermissionsMixin):
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (ADMIN,'Administrator')
    ]


    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True, max_length=225)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, null=True, blank=True)
    allergies = models.CharField(max_length=500, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
    blood_type = models.CharField(max_length=10,blank=True,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PATIENT)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timezone = models.CharField(max_length=200, blank=True, null=True)


    

    def display_age(self):
        if self.dob:
            try:
                if isinstance(self.dob, str):
                    dob_date = datetime.strptime(self.dob, '%Y-%m-%d').date()
                else:
                    dob_date = self.dob

                today = date.today()
                age = today.year - dob_date.year -((today.month, today.day) < (dob_date.month, dob_date.day))
                return age
            except (ValueError, TypeError):
                return None
            

        return None



    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return self.email





