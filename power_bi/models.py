from django.db import models
from users.models import User


class PowerBIDashboard(models.Model):
    """
    Model representing Power BI dashboards in the system.
    """
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    url_embed = models.URLField()
    departamento = models.CharField(max_length=100)
    visivel_para_roles = models.ManyToManyField(
        'users.Role',
        blank=True,
        related_name='powerbi_dashboards'
    )
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Dashboard Power BI"
        verbose_name_plural = "Dashboards Power BI"
    
    def __str__(self):
        return self.titulo