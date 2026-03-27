"""
URL configuration for sacip_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SACIP Backend API",
      default_version='v1',
      description="SACIP - Sistema de Apoio à Criminalidade e Investigação Policial",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@sacip.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', lambda request: redirect('schema-swagger-ui'), name='home'),
    path('admin/', admin.site.urls),
    re_path(r'^api/auth/?', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^api/informacoes-suspeitas/?', include('informacoes_suspeitas.urls')),
    re_path(r'^api/alvos-sob-investigacao/?', include('alvos_sob_investigacao.urls')),
    re_path(r'^api/power-bi/?', include('power_bi.urls')),
    re_path(r'^api/consulta-documentos/?', include('consulta_de_documentos.urls')),
    re_path(r'^api/monitoramento-viaturas/?', include('monitoramento_de_viaturas.urls')),
    re_path(r'^monitorizacao-redes-sociais/?', include('monitorizacao_de_redes_sociais.urls')),
    re_path(r'^api/criminalidade/?', include('criminalidade.urls')),
    re_path(r'^api/monitor-sos/?', include('monitor_sos.urls')),
    re_path(r'^api/cruzamento-dados/?', include('cruzamento_de_dados.urls')),
    re_path(r'^api/i2-analysis-notebook/?', include('i2_analysis_notebook.urls')),
    re_path(r'^api/relatorios/?', include('relatorios.urls')),
    re_path(r'^api/configuracoes/?', include('configuracoes.urls')),
    re_path(r'^api/analise-de-media-e-osint/?', include('analise_de_media_e_osint.urls')),
    re_path(r'^api/rss/?', include('servico_rss.urls')),
    re_path(r'^api/facial-recognition/?', include('facial_recognition.urls')),
    re_path(r'^api/angosite/?', include('invasao.urls')),
    re_path(r'^api/v1/sicgo/?', include('piips_integration.urls')),
    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in both development and production
# This is needed for drf-yasg and other static assets
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)