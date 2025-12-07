from django.contrib import admin
from .models import AlvoInvestigacao


@admin.register(AlvoInvestigacao)
class AlvoInvestigacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'status', 'nivel_prioridade', 'data_inicio')
    list_filter = ('status', 'nivel_prioridade', 'data_inicio')
    search_fields = ('nome', 'apelido', 'cpf')
    readonly_fields = ('data_inicio',)