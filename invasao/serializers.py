from rest_framework import serializers
from .models import IntrusionSession, CapturedMedia, IntrusionLog


class IntrusionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrusionSession
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class CapturedMediaSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()
    deviceInfo = serializers.ReadOnlyField(source='session.target_device')
    
    class Meta:
        model = CapturedMedia
        fields = ['id', 'session', 'media_type', 'file', 'imageUrl', 'deviceInfo', 'latitude', 'longitude', 'timestamp', 'caption', 'metadata']
        read_only_fields = ('timestamp',)
    
    def get_imageUrl(self, obj):
        """Return absolute URL for the file"""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            # Fallback if no request in context
            return obj.file.url
        return None


class IntrusionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntrusionLog
        fields = '__all__'
        read_only_fields = ('timestamp',)