from rest_framework import serializers
from .models import FonteDados, Cruzamento, Relacionamento


class FonteDadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FonteDados
        fields = '__all__'
        read_only_fields = ('data_criacao', 'criado_por')


class CruzamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cruzamento
        fields = '__all__'
        read_only_fields = ('data_execucao', 'executado_por', 'tempo_execucao_segundos')


class RelacionamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relacionamento
        fields = '__all__'
        read_only_fields = ('data_descoberta',)