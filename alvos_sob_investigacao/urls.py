from django.urls import re_path
from .views import AlvoInvestigacaoListCreateView, AlvoInvestigacaoRetrieveUpdateDestroyView, AlvoInvestigacaoUpdateDocumentoView, AddSuspectAsTargetView, SendTargetEmailView, SendTestEmailView, SendTargetSmsView, SendTestSmsView, SendTestSmsView, TargetCommunicationHistoryView, FirebaseDataView, FirestoreUsersView, send_sms_to_suspect, TargetFullHistoryView, AntecedenteCriminalListCreateView, AssociateOSINTView

urlpatterns = [
    re_path(r'^$', AlvoInvestigacaoListCreateView.as_view(), name='alvo-investigacao-list-create'),
    re_path(r'^(?P<pk>\d+)/?$', AlvoInvestigacaoRetrieveUpdateDestroyView.as_view(), name='alvo-investigacao-detail'),
    re_path(r'^(?P<pk>\d+)/update-documento/?$', AlvoInvestigacaoUpdateDocumentoView.as_view(), name='alvo-investigacao-update-documento'),
    re_path(r'^add-suspect/?$', AddSuspectAsTargetView.as_view(), name='add-suspect-as-target'),
    re_path(r'^(?P<pk>\d+)/send-email/?$', SendTargetEmailView.as_view(), name='send-target-email'),
    re_path(r'^send-test-email/?$', SendTestEmailView.as_view(), name='send-test-email'),
    re_path(r'^(?P<pk>\d+)/send-sms/?$', SendTargetSmsView.as_view(), name='send-target-sms'),
    re_path(r'^send-test-sms/?$', SendTestSmsView.as_view(), name='send-test-sms'),
    re_path(r'^send-sms-to-suspect/?$', send_sms_to_suspect, name='send-sms-to-suspect'),
    re_path(r'^(?P<pk>\d+)/communication-history/?$', TargetCommunicationHistoryView.as_view(), name='target-communication-history'),
    re_path(r'^(?P<alvo_id>\d+)/antecedentes/?$', AntecedenteCriminalListCreateView.as_view(), name='alvo-antecedentes'),
    re_path(r'^(?P<pk>\d+)/full-history/?$', TargetFullHistoryView.as_view(), name='target-full-history'),
    re_path(r'^associate-osint/?$', AssociateOSINTView.as_view(), name='associate-osint'),
    re_path(r'^firebase-data/?$', FirebaseDataView.as_view(), name='firebase-data'),
    re_path(r'^firestore-users/?$', FirestoreUsersView.as_view(), name='firestore-users'),
]
