from django.urls import path
from .views import DocumentoListCreateView, DocumentoRetrieveUpdateDestroyView, verificar_documento

urlpatterns = [
    path('consulta-documentos/', DocumentoListCreateView.as_view(), name='documento-list-create'),
    path('consulta-documentos/<int:pk>/', DocumentoRetrieveUpdateDestroyView.as_view(), name='documento-detail'),
    path('verificar/<str:numero>/', verificar_documento, name='verificar-documento'),
]