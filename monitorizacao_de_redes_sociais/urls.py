from django.urls import path
from .views import (
    PerfilRedeSocialListCreateView, 
    PerfilRedeSocialRetrieveUpdateDestroyView, 
    PostagemListCreateView, 
    PostagemRetrieveUpdateDestroyView,
    AlertaMonitoramentoListCreateView,
    AlertaMonitoramentoRetrieveUpdateDestroyView,
    sync_profile_data,
    sync_profile_posts,
    scrape_profile_and_posts,
    scrape_platform_posts,
    scrape_generic_content,
    get_atividades_monitorizadas,
    get_google_alerts_rss,
    add_google_alert,
    criar_alerta_monitoramento,
    buscar_resultados_alerta,
    buscar_todos_alertas_resultados,
    get_nossa_comunidade_users,
    sherlock_search,
    sherlock_search_stream,
    associar_perfil_alvo,
    listar_links_alvo,
    alvos_com_links,
)

urlpatterns = [
    path('perfis-redes-sociais/', PerfilRedeSocialListCreateView.as_view(), name='perfil-rede-social-list-create'),
    path('perfis-redes-sociais/<int:pk>/', PerfilRedeSocialRetrieveUpdateDestroyView.as_view(), name='perfil-rede-social-detail'),
    path('postagens/', PostagemListCreateView.as_view(), name='postagem-list-create'),
    path('postagens/<int:pk>/', PostagemRetrieveUpdateDestroyView.as_view(), name='postagem-detail'),
    path('alertas-monitoramento/', AlertaMonitoramentoListCreateView.as_view(), name='alerta-monitoramento-list-create'),
    path('alertas-monitoramento/<int:pk>/', AlertaMonitoramentoRetrieveUpdateDestroyView.as_view(), name='alerta-monitoramento-detail'),
    
    # Scraping endpoints
    path('perfis-redes-sociais/<int:perfil_id>/sync-profile/', sync_profile_data, name='sync-profile-data'),
    path('perfis-redes-sociais/<int:perfil_id>/sync-posts/', sync_profile_posts, name='sync-profile-posts'),
    path('perfis-redes-sociais/<int:perfil_id>/scrape/', scrape_profile_and_posts, name='scrape-profile-and-posts'),
    path('plataforma/<str:plataforma>/scrape/', scrape_platform_posts, name='scrape-platform-posts'),
    path('scrape-generic/', scrape_generic_content, name='scrape-generic-content'),
    
    # New endpoint for monitoring activities
    path('atividades/', get_atividades_monitorizadas, name='atividades-monitorizadas'),
    
    # Google Alerts endpoints
    path('google-alerts/', get_google_alerts_rss, name='google-alerts-rss'),
    path('google-alerts/add/', add_google_alert, name='add-google-alert'),
    
    # Alert monitoring endpoints
    path('alertas-monitoramento/criar/', criar_alerta_monitoramento, name='criar-alerta-monitoramento'),
    path('alertas-monitoramento/<int:alerta_id>/buscar-resultados/', buscar_resultados_alerta, name='buscar-resultados-alerta'),
    path('alertas-monitoramento/buscar-todos-resultados/', buscar_todos_alertas_resultados, name='buscar-todos-alertas-resultados'),
    path('nossa-comunidade/users/', get_nossa_comunidade_users, name='nossa-comunidade-users'),
    path('sherlock/', sherlock_search, name='sherlock-search'),
    path('sherlock/stream/', sherlock_search_stream, name='sherlock-search-stream'),
    path('alvos-redes-sociais/associar/', associar_perfil_alvo, name='associar-perfil-alvo'),
    path('alvos-redes-sociais/links/', listar_links_alvo, name='listar-links-alvo'),
    path('alvos-redes-sociais/alvos-com-links/', alvos_com_links, name='alvos-com-links'),
]