from django.contrib import admin
from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'nome_titular', 'data_criacao', 'ativo')
    list_filter = ('tipo', 'data_criacao', 'ativo')
    search_fields = ('numero', 'nome_titular')
    readonly_fields = ('data_criacao', 'data_atualizacao')