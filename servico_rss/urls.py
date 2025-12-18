from django.urls import path
from .views import FonteRSSListCreateView, FonteRSSDetailView, NoticiaRSSListView, ColetarNoticiasRSSView

urlpatterns = [
    path('fontes-rss/', FonteRSSListCreateView.as_view(), name='fonte-rss-list-create'),
    path('fontes-rss/<int:pk>/', FonteRSSDetailView.as_view(), name='fonte-rss-detail'),
    path('noticias-rss/', NoticiaRSSListView.as_view(), name='noticia-rss-list'),
    path('coletar-noticias/', ColetarNoticiasRSSView.as_view(), name='coletar-noticias-rss'),
]