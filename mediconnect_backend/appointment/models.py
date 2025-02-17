from django.db import models
import uuid
from account.models import User
from datetime import timedelta
from django.utils import timezone
from django.utils.timesince import timesince


class Appointment(models.Model):
    SENT = 'sent'
    PROCESSED = 'processed'
    IN_SESSION = 'in_session'
    DONE = 'done'
    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (PROCESSED, 'Processed'),
        (IN_SESSION, 'In_session'),
        (DONE, 'Done')
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    symptoms = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='appointment_by', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='appointment_for', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=SENT)
    follow_up_allowed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    @property
    def created_at_formatted(self):
        formatted = timesince(self.created_at)
        return str(formatted)

    @property
    def follow_up_expiry_date(self):
        expiry_date = self.created_at + timedelta(days=30)
        return expiry_date

    def can_book_follow_up(self):
        return self.follow_up_allowed and timezone.now() <= self.follow_up_expiry_date

