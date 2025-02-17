from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediconnect_backend.settings')

# Initialize Celery app for regular tasks
app = Celery('mediconnect_backend.regular_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Regular tasks configuration
app.conf.update(
    worker_pool="prefork",
    worker_prefetch_multiplier=4,
)

# Load tasks from your app
app.autodiscover_tasks(['appointment.regular_tasks'])