from django.urls import path

from . import apis

urlpatterns = [
   path('reminder/create/<uuid:id>/', apis.SetReminder.as_view(), name='set_reminder'),
   path('reminder/<uuid:id>/delete/', apis.DeleteReminder.as_view(), name='delete_reminder')
   
   
]