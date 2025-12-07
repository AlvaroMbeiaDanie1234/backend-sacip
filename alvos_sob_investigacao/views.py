from rest_framework import generics, permissions
from .models import AlvoInvestigacao
from .serializers import AlvoInvestigacaoSerializer


class AlvoInvestigacaoListCreateView(generics.ListCreateAPIView):
    queryset = AlvoInvestigacao.objects.all()
    serializer_class = AlvoInvestigacaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlvoInvestigacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlvoInvestigacao.objects.all()
    serializer_class = AlvoInvestigacaoSerializer
    permission_classes = [permissions.IsAuthenticated]