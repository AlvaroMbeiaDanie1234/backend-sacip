from rest_framework import serializers
from .models import FonteRSS, NoticiaRSS

class FonteRSSSerializer(serializers.ModelSerializer):
    class Meta:
        model = FonteRSS
        fields = '__all__'

class NoticiaRSSSerializer(serializers.ModelSerializer):
    fonte_nome = serializers.CharField(source='fonte.nome', read_only=True)
    
    class Meta:
        model = NoticiaRSS
        fields = '__all__'
        read_only_fields = ('data_coleta',)