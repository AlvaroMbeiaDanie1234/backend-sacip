from django.contrib import admin
from .models import PerfilRedeSocial, Postagem


@admin.register(PerfilRedeSocial)
class PerfilRedeSocialAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'plataforma', 'ativo', 'data_criacao')
    list_filter = ('plataforma', 'ativo', 'data_criacao')
    search_fields = ('nome_usuario', 'nome_completo')
    readonly_fields = ('data_criacao', 'data_ultima_atualizacao')


@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'data_postagem', 'curtidas', 'relevancia')
    list_filter = ('data_postagem', 'relevancia')
    search_fields = ('conteudo', 'perfil__nome_usuario')
    readonly_fields = ('data_coleta',)