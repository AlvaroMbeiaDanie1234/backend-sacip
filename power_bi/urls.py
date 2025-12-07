from django.urls import path
from .views import PowerBIDashboardListCreateView, PowerBIDashboardRetrieveUpdateDestroyView

urlpatterns = [
    path('power-bi/', PowerBIDashboardListCreateView.as_view(), name='power-bi-dashboard-list-create'),
    path('power-bi/<int:pk>/', PowerBIDashboardRetrieveUpdateDestroyView.as_view(), name='power-bi-dashboard-detail'),
]