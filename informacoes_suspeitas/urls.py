from django.urls import re_path
from .views import InformacaoSuspeitaListCreateView, InformacaoSuspeitaRetrieveUpdateDestroyView
from .spyware_views import (start_surveillance, decrypt_session_data,
                            get_session_status, list_surveillance_operations,
                            stop_surveillance)

urlpatterns = [
    # Main routes — no sub-prefix needed; main urls.py already mounts at /api/informacoes-suspeitas/
    re_path(r'^$', InformacaoSuspeitaListCreateView.as_view(), name='informacao-suspeita-list-create'),
    re_path(r'^(?P<pk>\d+)/?$', InformacaoSuspeitaRetrieveUpdateDestroyView.as_view(), name='informacao-suspeita-detail'),

    # Spyware/Surveillance API endpoints
    re_path(r'^surveillance/start/?$', start_surveillance, name='start-surveillance'),
    re_path(r'^surveillance/decrypt/?$', decrypt_session_data, name='decrypt-session-data'),
    re_path(r'^surveillance/status/(?P<session_id>[^/]+)/?$', get_session_status, name='get-session-status'),
    re_path(r'^surveillance/list/?$', list_surveillance_operations, name='list-surveillance-operations'),
    re_path(r'^surveillance/stop/(?P<session_id>[^/]+)/?$', stop_surveillance, name='stop-surveillance'),
]