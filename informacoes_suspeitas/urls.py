from django.urls import path
from .views import InformacaoSuspeitaListCreateView, InformacaoSuspeitaRetrieveUpdateDestroyView

urlpatterns = [
    path('informacoes-suspeitas/', InformacaoSuspeitaListCreateView.as_view(), name='informacao-suspeita-list-create'),
    path('informacoes-suspeitas/<int:pk>/', InformacaoSuspeitaRetrieveUpdateDestroyView.as_view(), name='informacao-suspeita-detail'),
]