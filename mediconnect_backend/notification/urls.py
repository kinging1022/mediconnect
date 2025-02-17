from django.urls import path
from . import apis

urlpatterns = [
    path('read/', apis.ReadNotification.as_view(), name='read'),
    path('read_all/',apis.ReadAllNotifications.as_view(), name='read_all'),
    

]