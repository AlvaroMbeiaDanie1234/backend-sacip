from rest_framework import generics, permissions
from .models import Viatura, RegistroMonitoramento
from .serializers import ViaturaSerializer, RegistroMonitoramentoSerializer


class ViaturaListCreateView(generics.ListCreateAPIView):
    queryset = Viatura.objects.all()
    serializer_class = ViaturaSerializer
    permission_classes = [permissions.IsAuthenticated]


class ViaturaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Viatura.objects.all()
    serializer_class = ViaturaSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistroMonitoramentoListCreateView(generics.ListCreateAPIView):
    queryset = RegistroMonitoramento.objects.all()
    serializer_class = RegistroMonitoramentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)


class RegistroMonitoramentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistroMonitoramento.objects.all()
    serializer_class = RegistroMonitoramentoSerializer
    permission_classes = [permissions.IsAuthenticated]