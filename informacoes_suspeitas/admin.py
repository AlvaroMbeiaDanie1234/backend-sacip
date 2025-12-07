from django.contrib import admin
from .models import InformacaoSuspeita


@admin.register(InformacaoSuspeita)
class InformacaoSuspeitaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fonte', 'nivel_confianca', 'data_criacao', 'ativo')
    list_filter = ('nivel_confianca', 'data_criacao', 'ativo', 'fonte')
    search_fields = ('titulo', 'descricao', 'fonte')
    readonly_fields = ('data_criacao', 'data_atualizacao')