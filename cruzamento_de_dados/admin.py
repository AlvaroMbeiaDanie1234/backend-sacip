from django.contrib import admin
from .models import FonteDados, Cruzamento, Relacionamento


@admin.register(FonteDados)
class FonteDadosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'ativo', 'data_criacao')
    list_filter = ('tipo', 'ativo', 'data_criacao')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('data_criacao',)


@admin.register(Cruzamento)
class CruzamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'data_execucao', 'tempo_execucao_segundos')
    list_filter = ('status', 'data_execucao')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('data_execucao', 'tempo_execucao_segundos')


@admin.register(Relacionamento)
class RelacionamentoAdmin(admin.ModelAdmin):
    list_display = ('cruzamento', 'entidade_a', 'entidade_b', 'tipo_relacionamento', 'grau_confianca')
    list_filter = ('tipo_relacionamento', 'grau_confianca')
    search_fields = ('entidade_a', 'entidade_b')
    readonly_fields = ('data_descoberta',)