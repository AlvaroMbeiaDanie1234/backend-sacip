from rest_framework import serializers
from .models import ConfiguracaoSistema, Auditoria, Notificacao, PermissaoCustomizada


class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoSistema
        fields = '__all__'


class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = '__all__'
        read_only_fields = ('data_hora', 'usuario')


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = '__all__'
        read_only_fields = ('data_criacao',)


class PermissaoCustomizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissaoCustomizada
        fields = '__all__'