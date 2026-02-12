from rest_framework import serializers
from .models import ConfiguracaoSistema, ConfiguracaoUsuario, Configuracao, TermoOfensivo
from users.models import User

class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoSistema
        fields = '__all__'

class ConfiguracaoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoUsuario
        fields = '__all__'

class ConfiguracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracao
        fields = '__all__'

class TermoOfensivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermoOfensivo
        fields = '__all__'
        read_only_fields = ('criado_em', 'atualizado_em', 'criado_por')

    def create(self, validated_data):
        # Set the user who created the term only if they are authenticated
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['criado_por'] = request.user
        return super().create(validated_data)