from rest_framework import generics, permissions
from .models import NotebookAnalise, EntidadeAnalise, ConexaoAnalise
from .serializers import NotebookAnaliseSerializer, EntidadeAnaliseSerializer, ConexaoAnaliseSerializer


class NotebookAnaliseListCreateView(generics.ListCreateAPIView):
    queryset = NotebookAnalise.objects.all()
    serializer_class = NotebookAnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class NotebookAnaliseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotebookAnalise.objects.all()
    serializer_class = NotebookAnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntidadeAnaliseListCreateView(generics.ListCreateAPIView):
    queryset = EntidadeAnalise.objects.all()
    serializer_class = EntidadeAnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntidadeAnaliseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntidadeAnalise.objects.all()
    serializer_class = EntidadeAnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConexaoAnaliseListCreateView(generics.ListCreateAPIView):
    queryset = ConexaoAnalise.objects.all()
    serializer_class = ConexaoAnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConexaoAnaliseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConexaoAnalise.objects.all()
    serializer_class = ConexaoAnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]