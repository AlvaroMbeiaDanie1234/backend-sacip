from django.urls import path
from .views import FonteDadosListCreateView, FonteDadosRetrieveUpdateDestroyView, CruzamentoListCreateView, CruzamentoRetrieveUpdateDestroyView, RelacionamentoListCreateView, RelacionamentoRetrieveUpdateDestroyView

urlpatterns = [
    path('fontes-dados/', FonteDadosListCreateView.as_view(), name='fonte-dados-list-create'),
    path('fontes-dados/<int:pk>/', FonteDadosRetrieveUpdateDestroyView.as_view(), name='fonte-dados-detail'),
    path('cruzamentos/', CruzamentoListCreateView.as_view(), name='cruzamento-list-create'),
    path('cruzamentos/<int:pk>/', CruzamentoRetrieveUpdateDestroyView.as_view(), name='cruzamento-detail'),
    path('relacionamentos/', RelacionamentoListCreateView.as_view(), name='relacionamento-list-create'),
    path('relacionamentos/<int:pk>/', RelacionamentoRetrieveUpdateDestroyView.as_view(), name='relacionamento-detail'),
]