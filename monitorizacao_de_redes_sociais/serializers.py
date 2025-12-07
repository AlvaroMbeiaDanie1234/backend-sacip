from rest_framework import serializers
from .models import PerfilRedeSocial, Postagem


class PerfilRedeSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilRedeSocial
        fields = '__all__'
        read_only_fields = ('data_criacao', 'data_ultima_atualizacao', 'monitorado_por')


class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        fields = '__all__'
        read_only_fields = ('data_coleta',)