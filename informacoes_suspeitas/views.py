from rest_framework import generics, permissions
from .models import InformacaoSuspeita
from .serializers import InformacaoSuspeitaSerializer


class InformacaoSuspeitaListCreateView(generics.ListCreateAPIView):
    queryset = InformacaoSuspeita.objects.all()
    serializer_class = InformacaoSuspeitaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class InformacaoSuspeitaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InformacaoSuspeita.objects.all()
    serializer_class = InformacaoSuspeitaSerializer
    permission_classes = [permissions.IsAuthenticated]