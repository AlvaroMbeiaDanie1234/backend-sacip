from rest_framework import serializers
from .models import InformacaoSuspeita


class InformacaoSuspeitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacaoSuspeita
        fields = '__all__'
        read_only_fields = ('data_criacao', 'data_atualizacao', 'criado_por')