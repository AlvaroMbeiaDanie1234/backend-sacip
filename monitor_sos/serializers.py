from rest_framework import serializers
from .models import ChamadaSOS, UnidadePolicial


class ChamadaSOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChamadaSOS
        fields = '__all__'
        read_only_fields = ('data_hora_chamada',)


class UnidadePolicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadePolicial
        fields = '__all__'
        read_only_fields = ('ultima_atualizacao',)