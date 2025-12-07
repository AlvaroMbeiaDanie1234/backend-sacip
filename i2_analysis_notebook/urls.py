from django.urls import path
from .views import NotebookAnaliseListCreateView, NotebookAnaliseRetrieveUpdateDestroyView, EntidadeAnaliseListCreateView, EntidadeAnaliseRetrieveUpdateDestroyView, ConexaoAnaliseListCreateView, ConexaoAnaliseRetrieveUpdateDestroyView

urlpatterns = [
    path('notebooks/', NotebookAnaliseListCreateView.as_view(), name='notebook-analise-list-create'),
    path('notebooks/<int:pk>/', NotebookAnaliseRetrieveUpdateDestroyView.as_view(), name='notebook-analise-detail'),
    path('entidades/', EntidadeAnaliseListCreateView.as_view(), name='entidade-analise-list-create'),
    path('entidades/<int:pk>/', EntidadeAnaliseRetrieveUpdateDestroyView.as_view(), name='entidade-analise-detail'),
    path('conexoes/', ConexaoAnaliseListCreateView.as_view(), name='conexao-analise-list-create'),
    path('conexoes/<int:pk>/', ConexaoAnaliseRetrieveUpdateDestroyView.as_view(), name='conexao-analise-detail'),
]