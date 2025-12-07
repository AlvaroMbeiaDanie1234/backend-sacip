from django.contrib import admin
from .models import TipoRelatorio, Relatorio, AgendamentoRelatorio


@admin.register(TipoRelatorio)
class TipoRelatorioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome', 'descricao')


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'formato', 'data_geracao', 'gerado_por')
    list_filter = ('tipo', 'formato', 'data_geracao')
    search_fields = ('titulo', 'conteudo')
    readonly_fields = ('data_geracao',)


@admin.register(AgendamentoRelatorio)
class AgendamentoRelatorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_relatorio', 'frequencia', 'hora_execucao', 'ativo')
    list_filter = ('frequencia', 'ativo', 'proxima_execucao')
    search_fields = ('nome',)
    readonly_fields = ('data_criacao',)