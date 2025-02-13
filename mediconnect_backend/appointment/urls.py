from django.urls import path
from . import apis

urlpatterns = [
    path('appointment/',apis.BookAppointmentOrFollow.as_view(), name='appointment'),
    path('confirm/follow-up/', apis.ConfirmFollowUp.as_view(), name='follow_up')
   

]

