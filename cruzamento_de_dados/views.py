from rest_framework import generics, permissions
from .models import FonteDados, Cruzamento, Relacionamento
from .serializers import FonteDadosSerializer, CruzamentoSerializer, RelacionamentoSerializer


class FonteDadosListCreateView(generics.ListCreateAPIView):
    queryset = FonteDados.objects.all()
    serializer_class = FonteDadosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class FonteDadosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FonteDados.objects.all()
    serializer_class = FonteDadosSerializer
    permission_classes = [permissions.IsAuthenticated]


class CruzamentoListCreateView(generics.ListCreateAPIView):
    queryset = Cruzamento.objects.all()
    serializer_class = CruzamentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(executado_por=self.request.user)


class CruzamentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cruzamento.objects.all()
    serializer_class = CruzamentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class RelacionamentoListCreateView(generics.ListCreateAPIView):
    queryset = Relacionamento.objects.all()
    serializer_class = RelacionamentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class RelacionamentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Relacionamento.objects.all()
    serializer_class = RelacionamentoSerializer
    permission_classes = [permissions.IsAuthenticated]