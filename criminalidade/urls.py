from django.urls import path
from .views import TipoCrimeListCreateView, TipoCrimeRetrieveUpdateDestroyView, OcorrenciaListCreateView, OcorrenciaRetrieveUpdateDestroyView, EnvolvidoListCreateView, EnvolvidoRetrieveUpdateDestroyView

urlpatterns = [
    path('tipos-crime/', TipoCrimeListCreateView.as_view(), name='tipo-crime-list-create'),
    path('tipos-crime/<int:pk>/', TipoCrimeRetrieveUpdateDestroyView.as_view(), name='tipo-crime-detail'),
    path('ocorrencias/', OcorrenciaListCreateView.as_view(), name='ocorrencia-list-create'),
    path('ocorrencias/<int:pk>/', OcorrenciaRetrieveUpdateDestroyView.as_view(), name='ocorrencia-detail'),
    path('envolvidos/', EnvolvidoListCreateView.as_view(), name='envolvido-list-create'),
    path('envolvidos/<int:pk>/', EnvolvidoRetrieveUpdateDestroyView.as_view(), name='envolvido-detail'),
]