from django.urls import path
from .views import ConfiguracaoSistemaListCreateView, ConfiguracaoSistemaRetrieveUpdateDestroyView, AuditoriaListCreateView, AuditoriaRetrieveUpdateDestroyView, NotificacaoListCreateView, NotificacaoRetrieveUpdateDestroyView, PermissaoCustomizadaListCreateView, PermissaoCustomizadaRetrieveUpdateDestroyView

urlpatterns = [
    path('configuracoes/', ConfiguracaoSistemaListCreateView.as_view(), name='configuracao-sistema-list-create'),
    path('configuracoes/<int:pk>/', ConfiguracaoSistemaRetrieveUpdateDestroyView.as_view(), name='configuracao-sistema-detail'),
    path('auditorias/', AuditoriaListCreateView.as_view(), name='auditoria-list-create'),
    path('auditorias/<int:pk>/', AuditoriaRetrieveUpdateDestroyView.as_view(), name='auditoria-detail'),
    path('notificacoes/', NotificacaoListCreateView.as_view(), name='notificacao-list-create'),
    path('notificacoes/<int:pk>/', NotificacaoRetrieveUpdateDestroyView.as_view(), name='notificacao-detail'),
    path('permissoes-customizadas/', PermissaoCustomizadaListCreateView.as_view(), name='permissao-customizada-list-create'),
    path('permissoes-customizadas/<int:pk>/', PermissaoCustomizadaRetrieveUpdateDestroyView.as_view(), name='permissao-customizada-detail'),
]