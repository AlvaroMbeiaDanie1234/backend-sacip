from rest_framework import serializers
from .models import PowerBIDashboard


class PowerBIDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerBIDashboard
        fields = '__all__'
        read_only_fields = ('data_criacao', 'data_atualizacao', 'criado_por')