from django.contrib import admin
from .models import ChamadaSOS, UnidadePolicial


@admin.register(ChamadaSOS)
class ChamadaSOSAdmin(admin.ModelAdmin):
    list_display = ('numero_origem', 'status', 'data_hora_chamada', 'prioridade')
    list_filter = ('status', 'prioridade', 'data_hora_chamada')
    search_fields = ('numero_origem', 'descricao')
    readonly_fields = ('data_hora_chamada',)


@admin.register(UnidadePolicial)
class UnidadePolicialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'disponivel', 'ultima_atualizacao')
    list_filter = ('tipo', 'disponivel')
    search_fields = ('nome', 'contato_radio')
    readonly_fields = ('ultima_atualizacao',)