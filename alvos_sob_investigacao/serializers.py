from rest_framework import serializers
from .models import AlvoInvestigacao


class AlvoInvestigacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlvoInvestigacao
        fields = '__all__'
        read_only_fields = ('data_inicio',)