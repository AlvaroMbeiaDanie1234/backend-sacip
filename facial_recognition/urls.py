from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^suspects/?$', views.SuspectListView.as_view(), name='suspect-list'),
    re_path(r'^suspects/(?P<pk>\d+)/?$', views.SuspectDetailView.as_view(), name='suspect-detail'),
    re_path(r'^camera-feeds/?$', views.CameraFeedListView.as_view(), name='camera-feed-list'),
    re_path(r'^camera-feeds/(?P<pk>\d+)/?$', views.CameraFeedDetailView.as_view(), name='camera-feed-detail'),
    re_path(r'^recognition-results/?$', views.RecognitionResultListView.as_view(), name='recognition-result-list'),
    re_path(r'^recognition-results/(?P<pk>\d+)/?$', views.RecognitionResultDetailView.as_view(), name='recognition-result-detail'),
    # unread MUST be before <pk> to avoid Django matching "unread" as an integer
    re_path(r'^alerts/unread/?$', views.UnreadAlertsView.as_view(), name='unread-alerts'),
    re_path(r'^alerts/?$', views.AlertListView.as_view(), name='alert-list'),
    re_path(r'^alerts/(?P<pk>\d+)/?$', views.AlertDetailView.as_view(), name='alert-detail'),
    re_path(r'^process-frame/?$', views.process_frame, name='process-frame'),
]