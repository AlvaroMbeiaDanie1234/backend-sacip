from django.urls import path
from .views import PerfilRedeSocialListCreateView, PerfilRedeSocialRetrieveUpdateDestroyView, PostagemListCreateView, PostagemRetrieveUpdateDestroyView

urlpatterns = [
    path('perfis-redes-sociais/', PerfilRedeSocialListCreateView.as_view(), name='perfil-rede-social-list-create'),
    path('perfis-redes-sociais/<int:pk>/', PerfilRedeSocialRetrieveUpdateDestroyView.as_view(), name='perfil-rede-social-detail'),
    path('postagens/', PostagemListCreateView.as_view(), name='postagem-list-create'),
    path('postagens/<int:pk>/', PostagemRetrieveUpdateDestroyView.as_view(), name='postagem-detail'),
]