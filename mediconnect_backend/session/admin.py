from django.contrib import admin
from .models import DoctorSession, DoctorSessionMessage

# Register your models here.

admin.site.register(DoctorSession)
admin.site.register(DoctorSessionMessage)
