from rest_framework import generics, permissions
from .models import TipoRelatorio, Relatorio, AgendamentoRelatorio
from .serializers import TipoRelatorioSerializer, RelatorioSerializer, AgendamentoRelatorioSerializer


class TipoRelatorioListCreateView(generics.ListCreateAPIView):
    queryset = TipoRelatorio.objects.all()
    serializer_class = TipoRelatorioSerializer
    permission_classes = [permissions.IsAuthenticated]


class TipoRelatorioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoRelatorio.objects.all()
    serializer_class = TipoRelatorioSerializer
    permission_classes = [permissions.IsAuthenticated]


class RelatorioListCreateView(generics.ListCreateAPIView):
    queryset = Relatorio.objects.all()
    serializer_class = RelatorioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(gerado_por=self.request.user)


class RelatorioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Relatorio.objects.all()
    serializer_class = RelatorioSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgendamentoRelatorioListCreateView(generics.ListCreateAPIView):
    queryset = AgendamentoRelatorio.objects.all()
    serializer_class = AgendamentoRelatorioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class AgendamentoRelatorioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AgendamentoRelatorio.objects.all()
    serializer_class = AgendamentoRelatorioSerializer
    permission_classes = [permissions.IsAuthenticated]