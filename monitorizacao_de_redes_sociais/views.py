from rest_framework import generics, permissions
from .models import PerfilRedeSocial, Postagem
from .serializers import PerfilRedeSocialSerializer, PostagemSerializer


class PerfilRedeSocialListCreateView(generics.ListCreateAPIView):
    queryset = PerfilRedeSocial.objects.all()
    serializer_class = PerfilRedeSocialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(monitorado_por=self.request.user)


class PerfilRedeSocialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerfilRedeSocial.objects.all()
    serializer_class = PerfilRedeSocialSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostagemListCreateView(generics.ListCreateAPIView):
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostagemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer
    permission_classes = [permissions.IsAuthenticated]