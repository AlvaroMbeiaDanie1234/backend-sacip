from django.contrib import admin
from .models import Viatura, RegistroMonitoramento


@admin.register(Viatura)
class ViaturaAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'marca', 'ano', 'status')
    list_filter = ('status', 'marca', 'ano')
    search_fields = ('placa', 'modelo', 'renavam', 'chassi')
    readonly_fields = ('data_criacao', 'data_atualizacao')


@admin.register(RegistroMonitoramento)
class RegistroMonitoramentoAdmin(admin.ModelAdmin):
    list_display = ('viatura', 'latitude', 'longitude', 'data_registro')
    list_filter = ('data_registro',)
    search_fields = ('viatura__placa',)
    readonly_fields = ('data_registro',)