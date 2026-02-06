from django.urls import path
from .views import AlvoInvestigacaoListCreateView, AlvoInvestigacaoRetrieveUpdateDestroyView, AlvoInvestigacaoUpdateDocumentoView, AddSuspectAsTargetView, SendTargetEmailView, SendTestEmailView, SendTargetSmsView, SendTestSmsView, FirebaseDataView, FirestoreUsersView, send_sms_to_suspect

urlpatterns = [
    path('alvos-sob-investigacao/', AlvoInvestigacaoListCreateView.as_view(), name='alvo-investigacao-list-create'),
    path('alvos-sob-investigacao/<int:pk>/', AlvoInvestigacaoRetrieveUpdateDestroyView.as_view(), name='alvo-investigacao-detail'),
    path('alvos-sob-investigacao/<int:pk>/update-documento/', AlvoInvestigacaoUpdateDocumentoView.as_view(), name='alvo-investigacao-update-documento'),
    path('alvos-sob-investigacao/add-suspect/', AddSuspectAsTargetView.as_view(), name='add-suspect-as-target'),
    path('alvos-sob-investigacao/<int:pk>/send-email/', SendTargetEmailView.as_view(), name='send-target-email'),
    path('alvos-sob-investigacao/send-test-email/', SendTestEmailView.as_view(), name='send-test-email'),
    path('alvos-sob-investigacao/<int:pk>/send-sms/', SendTargetSmsView.as_view(), name='send-target-sms'),
    path('alvos-sob-investigacao/send-test-sms/', SendTestSmsView.as_view(), name='send-test-sms'),
    path('alvos-sob-investigacao/send-sms-to-suspect/', send_sms_to_suspect, name='send-sms-to-suspect'),
    path('alvos-sob-investigacao/firebase-data/', FirebaseDataView.as_view(), name='firebase-data'),
    path('firestore-users/', FirestoreUsersView.as_view(), name='firestore-users'),
]
