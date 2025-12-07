from django.urls import path
from .views import osint_search

urlpatterns = [
    path('osint-search/', osint_search, name='osint-search'),
]