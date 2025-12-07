from django.contrib import admin
from .models import ConfiguracaoSistema, Auditoria, Notificacao, PermissaoCustomizada


@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('chave', 'valor', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('chave', 'descricao')


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'modelo', 'data_hora')
    list_filter = ('acao', 'data_hora', 'modelo')
    search_fields = ('usuario__username', 'descricao')
    readonly_fields = ('data_hora',)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao', 'importante')
    list_filter = ('importante', 'data_criacao')
    search_fields = ('titulo', 'mensagem')
    readonly_fields = ('data_criacao',)


@admin.register(PermissaoCustomizada)
class PermissaoCustomizadaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo')
    search_fields = ('nome', 'codigo', 'descricao')