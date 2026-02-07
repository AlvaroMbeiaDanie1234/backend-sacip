from django.urls import path
from .views import AlvoInvestigacaoListCreateView, AlvoInvestigacaoRetrieveUpdateDestroyView, AlvoInvestigacaoUpdateDocumentoView, AddSuspectAsTargetView, SendTargetEmailView, SendTestEmailView, SendTargetSmsView, SendTestSmsView, TargetCommunicationHistoryView, FirebaseDataView, FirestoreUsersView, send_sms_to_suspect

urlpatterns = [
    path('', AlvoInvestigacaoListCreateView.as_view(), name='alvo-investigacao-list-create'),
    path('<int:pk>/', AlvoInvestigacaoRetrieveUpdateDestroyView.as_view(), name='alvo-investigacao-detail'),
    path('<int:pk>/update-documento/', AlvoInvestigacaoUpdateDocumentoView.as_view(), name='alvo-investigacao-update-documento'),
    path('add-suspect/', AddSuspectAsTargetView.as_view(), name='add-suspect-as-target'),
    path('<int:pk>/send-email/', SendTargetEmailView.as_view(), name='send-target-email'),
    path('send-test-email/', SendTestEmailView.as_view(), name='send-test-email'),
    path('<int:pk>/send-sms/', SendTargetSmsView.as_view(), name='send-target-sms'),
    path('send-test-sms/', SendTestSmsView.as_view(), name='send-test-sms'),
    path('send-sms-to-suspect/', send_sms_to_suspect, name='send-sms-to-suspect'),
    path('<int:pk>/communication-history/', TargetCommunicationHistoryView.as_view(), name='target-communication-history'),
    path('firebase-data/', FirebaseDataView.as_view(), name='firebase-data'),
    path('firestore-users/', FirestoreUsersView.as_view(), name='firestore-users'),
]
