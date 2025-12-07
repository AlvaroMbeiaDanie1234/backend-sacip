from django.urls import path
from .views import ChamadaSOSListCreateView, ChamadaSOSRetrieveUpdateDestroyView, UnidadePolicialListCreateView, UnidadePolicialRetrieveUpdateDestroyView

urlpatterns = [
    path('chamadas-sos/', ChamadaSOSListCreateView.as_view(), name='chamada-sos-list-create'),
    path('chamadas-sos/<int:pk>/', ChamadaSOSRetrieveUpdateDestroyView.as_view(), name='chamada-sos-detail'),
    path('unidades-policiais/', UnidadePolicialListCreateView.as_view(), name='unidade-policial-list-create'),
    path('unidades-policiais/<int:pk>/', UnidadePolicialRetrieveUpdateDestroyView.as_view(), name='unidade-policial-detail'),
]