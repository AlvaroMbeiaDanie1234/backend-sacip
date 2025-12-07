from rest_framework import generics, permissions
from .models import ChamadaSOS, UnidadePolicial
from .serializers import ChamadaSOSSerializer, UnidadePolicialSerializer


class ChamadaSOSListCreateView(generics.ListCreateAPIView):
    queryset = ChamadaSOS.objects.all()
    serializer_class = ChamadaSOSSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChamadaSOSRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChamadaSOS.objects.all()
    serializer_class = ChamadaSOSSerializer
    permission_classes = [permissions.IsAuthenticated]


class UnidadePolicialListCreateView(generics.ListCreateAPIView):
    queryset = UnidadePolicial.objects.all()
    serializer_class = UnidadePolicialSerializer
    permission_classes = [permissions.IsAuthenticated]


class UnidadePolicialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnidadePolicial.objects.all()
    serializer_class = UnidadePolicialSerializer
    permission_classes = [permissions.IsAuthenticated]