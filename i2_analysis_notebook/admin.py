from django.contrib import admin
from .models import NotebookAnalise, EntidadeAnalise, ConexaoAnalise


@admin.register(NotebookAnalise)
class NotebookAnaliseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'criado_por', 'data_criacao', 'publico')
    list_filter = ('publico', 'data_criacao')
    search_fields = ('titulo', 'descricao')
    readonly_fields = ('data_criacao', 'data_ultima_edicao')


@admin.register(EntidadeAnalise)
class EntidadeAnaliseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'notebook')
    list_filter = ('tipo',)
    search_fields = ('nome', 'dados')


@admin.register(ConexaoAnalise)
class ConexaoAnaliseAdmin(admin.ModelAdmin):
    list_display = ('origem', 'destino', 'tipo_conexao', 'peso')
    list_filter = ('tipo_conexao',)
    search_fields = ('tipo_conexao', 'descricao')