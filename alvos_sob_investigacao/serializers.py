from rest_framework import serializers
from .models import AlvoInvestigacao, CommunicationHistory


class AlvoInvestigacaoSerializer(serializers.ModelSerializer):
    # Map numero_identificacao from frontend to cpf in the model
    numero_identificacao = serializers.CharField(source='cpf', required=False, allow_blank=True)
    
    class Meta:
        model = AlvoInvestigacao
        fields = '__all__'
        read_only_fields = ('data_inicio',)
    
    # Override to handle the mapping in the other direction
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Map cpf from model to numero_identificacao for frontend
        representation['numero_identificacao'] = representation.pop('cpf', '')
        return representation


class CommunicationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationHistory
        fields = '__all__'
        read_only_fields = ('sent_at',)


class CommunicationHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationHistory
        fields = ['target', 'communication_type', 'recipient', 'subject', 'message', 'sent_by', 'status', 'response', 'external_reference']


class CommunicationHistoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationHistory
        fields = ['id', 'communication_type', 'recipient', 'subject', 'sent_at', 'status']