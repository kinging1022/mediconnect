# Generated by Django 5.1.6 on 2025-02-22 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_emergency_contact_user_emergency_contact_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timezone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
