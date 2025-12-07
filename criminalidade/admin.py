from django.contrib import admin
from .models import TipoCrime, Ocorrencia, Envolvido


@admin.register(TipoCrime)
class TipoCrimeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_penal')
    search_fields = ('nome', 'codigo_penal')


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ('tipo_crime', 'data_ocorrencia', 'cidade', 'status', 'nivel_gravidade')
    list_filter = ('status', 'nivel_gravidade', 'cidade', 'tipo_crime')
    search_fields = ('descricao', 'endereco', 'bairro')
    readonly_fields = ('data_registro',)
    date_hierarchy = 'data_ocorrencia'


@admin.register(Envolvido)
class EnvolvidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_envolvimento', 'ocorrencia')
    list_filter = ('tipo_envolvimento',)
    search_fields = ('nome', 'ocorrencia__descricao')