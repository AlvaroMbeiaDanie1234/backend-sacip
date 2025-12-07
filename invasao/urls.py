from django.urls import path
from django.views.generic import TemplateView
from .views import (
    invasion_page, 
    football_template, 
    prizes_template, 
    adult_template, 
    news_template,
    PublicMediaUploadView, 
    IntrusionSessionListCreateView, 
    IntrusionSessionRetrieveUpdateDestroyView, 
    CapturedMediaListCreateView, 
    CapturedMediaRetrieveUpdateDestroyView, 
    IntrusionLogListCreateView, 
    IntrusionLogRetrieveUpdateDestroyView,
    get_captures_by_suspect,
    get_sessions,
    search_similar_images  # Adicionando a nova view
)

urlpatterns = [
    path('', invasion_page, name='invasion-page'),
    path('football/', football_template, name='football-template'),
    path('prizes/', prizes_template, name='prizes-template'),
    path('adult/', adult_template, name='adult-template'),
    path('news/', news_template, name='news-template'),
    path('upload/', PublicMediaUploadView.as_view(), name='public-media-upload'),
    path('captures/', get_captures_by_suspect, name='get-captures-by-suspect'),
    path('debug/sessions/', get_sessions, name='get-sessions'),
    path('sessions/', IntrusionSessionListCreateView.as_view(), name='intrusion-session-list-create'),
    path('sessions/<int:pk>/', IntrusionSessionRetrieveUpdateDestroyView.as_view(), name='intrusion-session-detail'),
    path('media/', CapturedMediaListCreateView.as_view(), name='captured-media-list-create'),
    path('media/<int:pk>/', CapturedMediaRetrieveUpdateDestroyView.as_view(), name='captured-media-detail'),
    path('logs/', IntrusionLogListCreateView.as_view(), name='intrusion-log-list-create'),
    path('logs/<int:pk>/', IntrusionLogRetrieveUpdateDestroyView.as_view(), name='intrusion-log-detail'),
    path('search-similar-images/', search_similar_images, name='search-similar-images'),  # Nova rota corrigida
]