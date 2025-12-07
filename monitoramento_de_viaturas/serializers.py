from rest_framework import serializers
from .models import Viatura, RegistroMonitoramento


class ViaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viatura
        fields = '__all__'
        read_only_fields = ('data_criacao', 'data_atualizacao')


class RegistroMonitoramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroMonitoramento
        fields = '__all__'
        read_only_fields = ('data_registro',)