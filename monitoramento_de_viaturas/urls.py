from django.urls import path
from .views import ViaturaListCreateView, ViaturaRetrieveUpdateDestroyView, RegistroMonitoramentoListCreateView, RegistroMonitoramentoRetrieveUpdateDestroyView

urlpatterns = [
    path('viaturas/', ViaturaListCreateView.as_view(), name='viatura-list-create'),
    path('viaturas/<int:pk>/', ViaturaRetrieveUpdateDestroyView.as_view(), name='viatura-detail'),
    path('registros-monitoramento/', RegistroMonitoramentoListCreateView.as_view(), name='registro-monitoramento-list-create'),
    path('registros-monitoramento/<int:pk>/', RegistroMonitoramentoRetrieveUpdateDestroyView.as_view(), name='registro-monitoramento-detail'),
]