from django.contrib import admin
from .models import IntrusionSession, CapturedMedia, IntrusionLog


@admin.register(IntrusionSession)
class IntrusionSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_device', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at', 'target_device')
    search_fields = ('title', 'description', 'target_device')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CapturedMedia)
class CapturedMediaAdmin(admin.ModelAdmin):
    list_display = ('session', 'media_type', 'caption', 'timestamp', 'file_size')
    list_filter = ('media_type', 'timestamp')
    search_fields = ('caption', 'session__title')
    readonly_fields = ('timestamp',)


@admin.register(IntrusionLog)
class IntrusionLogAdmin(admin.ModelAdmin):
    list_display = ('session', 'event_type', 'severity', 'timestamp')
    list_filter = ('severity', 'timestamp', 'event_type')
    search_fields = ('description', 'session__title')
    readonly_fields = ('timestamp',)