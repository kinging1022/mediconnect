# Generated by Django 5.1.6 on 2025-02-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('appointment', 'Appointment'), ('consultation', 'Consultation'), ('message', 'Message'), ('session_start', 'Session_start'), ('session_stop', 'Session_stop')], max_length=50),
        ),
    ]
