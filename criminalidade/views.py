from rest_framework import generics, permissions
from .models import TipoCrime, Ocorrencia, Envolvido
from .serializers import TipoCrimeSerializer, OcorrenciaSerializer, EnvolvidoSerializer


class TipoCrimeListCreateView(generics.ListCreateAPIView):
    queryset = TipoCrime.objects.all()
    serializer_class = TipoCrimeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TipoCrimeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoCrime.objects.all()
    serializer_class = TipoCrimeSerializer
    permission_classes = [permissions.IsAuthenticated]


class OcorrenciaListCreateView(generics.ListCreateAPIView):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)


class OcorrenciaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer
    permission_classes = [permissions.IsAuthenticated]


class EnvolvidoListCreateView(generics.ListCreateAPIView):
    queryset = Envolvido.objects.all()
    serializer_class = EnvolvidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class EnvolvidoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Envolvido.objects.all()
    serializer_class = EnvolvidoSerializer
    permission_classes = [permissions.IsAuthenticated]