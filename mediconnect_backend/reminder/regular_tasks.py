from celery import shared_task

from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Reminder
import pytz
from datetime import datetime
from django.conf import settings

@shared_task(queue='regular_tasks')
def send_daily_reminders():
    current_time_utc = now()

    reminders = Reminder.objects.filter(sent=False)

    print(f"Reminder found: {reminders.count()}")
    print(f"Cureent utc time {current_time_utc.time()}")


    for reminder in reminders:
        try:
            user_timezone = pytz.timezone(reminder.user.timezone or 'UTC')

            current_date_user = current_time_utc.astimezone(user_timezone).date()
            reminder_datetime_user = datetime.combine(current_date_user, reminder.time)
            reminder_datetime_user = user_timezone.localize(reminder_datetime_user)

            reminder_datetime_utc = reminder_datetime_user.astimezone(pytz.utc)

            print(f'Reminder time in UTC: {reminder_datetime_utc}')

            if(current_time_utc.hour == reminder_datetime_utc.hour and
               
               current_time_utc.minute == reminder_datetime_utc.minute
               
               ):
                
                send_mail(
                     "Daily Reminder",
                    reminder.message,
                    'from@example.com',
                    [reminder.email]
                )

                #if reminder.phone:
                    #send_text_reminder.delay(reminder.phone, reminder.message)

                reminder.sent = True
                reminder.save()



            

        except Exception as e:
            print(f"Failed to send reminder {reminder.id}: {e}")


            


@shared_task(queue = 'regular_tasks')
def reset_sent_status():
    Reminder.objects.filter(sent=True).update(sent=False)
    
    
@shared_task(queue='regular_tasks')
def send_text_reminder(to_phone, message):
    from twilio.rest import Client
    client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_='+17755725905',
        to=to_phone
    )