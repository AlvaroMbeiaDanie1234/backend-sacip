from django.urls import path
from .views import TipoRelatorioListCreateView, TipoRelatorioRetrieveUpdateDestroyView, RelatorioListCreateView, RelatorioRetrieveUpdateDestroyView, AgendamentoRelatorioListCreateView, AgendamentoRelatorioRetrieveUpdateDestroyView

urlpatterns = [
    path('tipos-relatorio/', TipoRelatorioListCreateView.as_view(), name='tipo-relatorio-list-create'),
    path('tipos-relatorio/<int:pk>/', TipoRelatorioRetrieveUpdateDestroyView.as_view(), name='tipo-relatorio-detail'),
    path('relatorios/', RelatorioListCreateView.as_view(), name='relatorio-list-create'),
    path('relatorios/<int:pk>/', RelatorioRetrieveUpdateDestroyView.as_view(), name='relatorio-detail'),
    path('agendamentos-relatorio/', AgendamentoRelatorioListCreateView.as_view(), name='agendamento-relatorio-list-create'),
    path('agendamentos-relatorio/<int:pk>/', AgendamentoRelatorioRetrieveUpdateDestroyView.as_view(), name='agendamento-relatorio-detail'),
]