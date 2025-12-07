from rest_framework import generics, permissions
from .models import PowerBIDashboard
from .serializers import PowerBIDashboardSerializer


class PowerBIDashboardListCreateView(generics.ListCreateAPIView):
    queryset = PowerBIDashboard.objects.all()
    serializer_class = PowerBIDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class PowerBIDashboardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PowerBIDashboard.objects.all()
    serializer_class = PowerBIDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]