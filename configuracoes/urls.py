from django.urls import path
from . import views

urlpatterns = [
    # Configurações do Sistema
    path('sistema/', views.ConfiguracaoSistemaListView.as_view(), name='configuracao-sistema-list'),
    path('sistema/<int:pk>/', views.ConfiguracaoSistemaDetailView.as_view(), name='configuracao-sistema-detail'),

    # Configurações do Usuário
    path('usuarios/', views.ConfiguracaoUsuarioListView.as_view(), name='configuracao-usuario-list'),
    path('usuarios/<int:pk>/', views.ConfiguracaoUsuarioDetailView.as_view(), name='configuracao-usuario-detail'),

    # Configurações Gerais
    path('gerais/', views.ConfiguracaoListView.as_view(), name='configuracao-list'),
    path('gerais/<int:pk>/', views.ConfiguracaoDetailView.as_view(), name='configuracao-detail'),

    # Dicionário de Termos Ofensivos
    path('termos-ofensivos/', views.TermoOfensivoListView.as_view(), name='termo-ofensivo-list'),
    path('termos-ofensivos/<int:pk>/', views.TermoOfensivoDetailView.as_view(), name='termo-ofensivo-detail'),
    path('termos-ofensivos/public/', views.get_termos_ofensivos_public, name='termos-ofensivos-public'),
    path('termos-ofensivos/severidade/', views.get_termos_ofensivos_by_severity, name='termos-ofensivos-by-severity'),
    
    # Mock endpoints for testing
    path('termos-ofensivos-mock/', views.get_termos_ofensivos_mock, name='termos-ofensivos-mock'),
    path('termos-ofensivos-mock/create/', views.create_termo_ofensivo_mock, name='termos-ofensivos-create-mock'),
    path('termos-ofensivos-mock/<int:pk>/update/', views.update_termo_ofensivo_mock, name='termos-ofensivos-update-mock'),
    path('termos-ofensivos-mock/<int:pk>/delete/', views.delete_termo_ofensivo_mock, name='termos-ofensivos-delete-mock'),
]