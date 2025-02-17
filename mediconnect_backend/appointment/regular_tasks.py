from celery_config.regular_tasks import app

@app.task(queue='regular_tasks')
def send_notification(user_id):
    # Your regular task code here
    pass