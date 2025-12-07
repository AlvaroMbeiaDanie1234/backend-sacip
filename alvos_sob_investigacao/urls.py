from django.urls import path
from .views import AlvoInvestigacaoListCreateView, AlvoInvestigacaoRetrieveUpdateDestroyView

urlpatterns = [
    path('alvos-sob-investigacao/', AlvoInvestigacaoListCreateView.as_view(), name='alvo-investigacao-list-create'),
    path('alvos-sob-investigacao/<int:pk>/', AlvoInvestigacaoRetrieveUpdateDestroyView.as_view(), name='alvo-investigacao-detail'),
]