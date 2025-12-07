from rest_framework import serializers
from .models import IntrusionSession, CapturedMedia, IntrusionLog


class IntrusionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrusionSession
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class CapturedMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapturedMedia
        fields = '__all__'
        read_only_fields = ('timestamp',)


class IntrusionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrusionLog
        fields = '__all__'
        read_only_fields = ('timestamp',)