from rest_framework import serializers
from .models import TipoCrime, Ocorrencia, Envolvido


class TipoCrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCrime
        fields = '__all__'


class OcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocorrencia
        fields = '__all__'
        read_only_fields = ('data_registro', 'registrado_por')


class EnvolvidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envolvido
        fields = '__all__'