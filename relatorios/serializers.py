from rest_framework import serializers
from .models import TipoRelatorio, Relatorio, AgendamentoRelatorio


class TipoRelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRelatorio
        fields = '__all__'


class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = '__all__'
        read_only_fields = ('data_geracao', 'gerado_por')


class AgendamentoRelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendamentoRelatorio
        fields = '__all__'
        read_only_fields = ('data_criacao', 'criado_por', 'ultima_execucao')