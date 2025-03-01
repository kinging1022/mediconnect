from django.urls import path
from . import apis

urlpatterns = [
    path('session/start/',apis.GetOrCreateSession.as_view(), name='start_session'),
    path('session/active/', apis.GetActiveSession.as_view(), name='active_session'),
    path('session/messages/', apis.GetSessionMessages.as_view(), name='session_messages'),
    path('sessions/medications/<uuid:id>/', apis.AddMedications.as_view(), name='add_medication'),
    path('sessions/followup/<uuid:id>/', apis.AddFollowup.as_view(), name='add_followup'),
    path('session/history/', apis.SessionHistory.as_view(), name='session-history' ),
    path('session/', apis.ViewSession.as_view(), name='session'),
    path('sessions/<uuid:session_id>/upload/', apis.UploadFile.as_view(), name='upload'),
    path('session/agora/token/', apis.GetAgoraToken.as_view(), name='agora_token')

    

]