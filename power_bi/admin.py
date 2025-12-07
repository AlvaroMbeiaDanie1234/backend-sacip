from django.contrib import admin
from .models import PowerBIDashboard


@admin.register(PowerBIDashboard)
class PowerBIDashboardAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'departamento', 'ativo', 'data_criacao')
    list_filter = ('departamento', 'ativo', 'data_criacao')
    search_fields = ('titulo', 'departamento')
    readonly_fields = ('data_criacao', 'data_atualizacao')