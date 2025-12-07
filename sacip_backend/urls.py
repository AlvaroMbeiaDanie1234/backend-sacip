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
from django.urls import path, include
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
    path('api/auth/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/informacoes-suspeitas/', include('informacoes_suspeitas.urls')),
    path('api/alvos-sob-investigacao/', include('alvos_sob_investigacao.urls')),
    path('api/power-bi/', include('power_bi.urls')),
    path('api/consulta-documentos/', include('consulta_de_documentos.urls')),
    path('api/monitoramento-viaturas/', include('monitoramento_de_viaturas.urls')),
    path('api/monitorizacao-redes-sociais/', include('monitorizacao_de_redes_sociais.urls')),
    path('api/criminalidade/', include('criminalidade.urls')),
    path('api/monitor-sos/', include('monitor_sos.urls')),
    path('api/cruzamento-dados/', include('cruzamento_de_dados.urls')),
    path('api/i2-analysis-notebook/', include('i2_analysis_notebook.urls')),
    path('api/relatorios/', include('relatorios.urls')),
    path('api/configuracoes/', include('configuracoes.urls')),
    path('api/invasao/', include('invasao.urls')),
    path('api/analise-de-media-e-osint/', include('analise_de_media_e_osint.urls')),    
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