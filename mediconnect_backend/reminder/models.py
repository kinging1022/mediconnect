from django.db import models
from account.models import User
from session.models import Medications
import uuid

# Create your models here.
class Reminder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False )
    user = models.ForeignKey(User, related_name='reminder', on_delete=models.CASCADE)
    medication = models.ForeignKey(Medications, related_name='reminder', on_delete=models.CASCADE)
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    sent = models.BooleanField(default=False) 