from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediconnect_backend.settings')

# Initialize Celery app
app = Celery('mediconnect_backend')

# Load Celery settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Define task routing (Queues)
app.conf.task_routes = {
    'appointment.ml_tasks.*': {'queue': 'ml_tasks'},
    'reminder.regular_tasks.*': {'queue': 'regular_tasks'}
}

# Set the default queue for tasks that don’t specify one
app.conf.task_default_queue = 'regular_tasks'

# Auto-discover tasks in Django apps (removes need for manual imports)
app.autodiscover_tasks(['appointment.ml_tasks', 'reminder.regular_tasks'])
