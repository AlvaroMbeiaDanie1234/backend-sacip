from rest_framework import serializers
from .models import PerfilRedeSocial, Postagem, AlertaMonitoramento, LinkRedeSocialAlvo


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


class AlertaMonitoramentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaMonitoramento
        fields = '__all__'
        read_only_fields = ('data_criacao', 'data_ultima_verificacao', 'monitorado_por')


class LinkRedeSocialAlvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkRedeSocialAlvo
        fields = ('id', 'alvo_id', 'nome_site', 'url_perfil', 'data_associacao')
        read_only_fields = ('data_associacao',)