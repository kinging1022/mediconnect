from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# ML-specific environment settings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mediconnect_backend.settings')

# Initialize Celery app for ML tasks
app = Celery('mediconnect_backend.ml_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

# ML-specific configuration
app.conf.update(
    worker_pool="solo",
    task_time_limit=300,
    worker_max_tasks_per_child=10,
)

# Load tasks from your app
app.autodiscover_tasks(['appointment.ml_tasks'])