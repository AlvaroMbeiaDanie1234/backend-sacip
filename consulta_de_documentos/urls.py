from django.urls import path
from .views import DocumentoListCreateView, DocumentoRetrieveUpdateDestroyView

urlpatterns = [
    path('consulta-documentos/', DocumentoListCreateView.as_view(), name='documento-list-create'),
    path('consulta-documentos/<int:pk>/', DocumentoRetrieveUpdateDestroyView.as_view(), name='documento-detail'),
]