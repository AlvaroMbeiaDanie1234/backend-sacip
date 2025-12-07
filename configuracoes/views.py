from rest_framework import generics, permissions
from .models import ConfiguracaoSistema, Auditoria, Notificacao, PermissaoCustomizada
from .serializers import ConfiguracaoSistemaSerializer, AuditoriaSerializer, NotificacaoSerializer, PermissaoCustomizadaSerializer


class ConfiguracaoSistemaListCreateView(generics.ListCreateAPIView):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConfiguracaoSistemaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuditoriaListCreateView(generics.ListCreateAPIView):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuditoriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificacaoListCreateView(generics.ListCreateAPIView):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PermissaoCustomizadaListCreateView(generics.ListCreateAPIView):
    queryset = PermissaoCustomizada.objects.all()
    serializer_class = PermissaoCustomizadaSerializer
    permission_classes = [permissions.IsAuthenticated]


class PermissaoCustomizadaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PermissaoCustomizada.objects.all()
    serializer_class = PermissaoCustomizadaSerializer
    permission_classes = [permissions.IsAuthenticated]