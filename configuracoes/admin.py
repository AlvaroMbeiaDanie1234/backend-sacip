from django.contrib import admin
from .models import ConfiguracaoSistema, ConfiguracaoUsuario, Configuracao, TermoOfensivo

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ['chave', 'valor', 'descricao', 'criado_em', 'atualizado_em']
    list_filter = ['chave', 'criado_em']
    search_fields = ['chave', 'valor']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ConfiguracaoUsuario)
class ConfiguracaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'chave', 'valor', 'criado_em', 'atualizado_em']
    list_filter = ['usuario', 'chave', 'criado_em']
    search_fields = ['usuario__username', 'chave', 'valor']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ['chave', 'valor', 'descricao', 'usuario', 'criado_em', 'atualizado_em']
    list_filter = ['usuario', 'criado_em']
    search_fields = ['chave', 'valor', 'usuario__username']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(TermoOfensivo)
class TermoOfensivoAdmin(admin.ModelAdmin):
    list_display = ['termo', 'nivel_severidade', 'ativo', 'criado_por', 'criado_em']
    list_filter = ['ativo', 'nivel_severidade', 'criado_em']
    search_fields = ['termo', 'descricao', 'criado_por__username']
    readonly_fields = ['criado_em', 'atualizado_em', 'criado_por']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If object is being created
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)