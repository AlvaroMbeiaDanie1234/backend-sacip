from django.db import models
from users.models import User


class Viatura(models.Model):
    """
    Model representing vehicles in the monitoring system.
    """
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    renavam = models.CharField(max_length=20, unique=True)
    chassi = models.CharField(max_length=20, unique=True)
    proprietario = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativo', 'Ativo'),
            ('inativo', 'Inativo'),
            ('roubo', 'Roubo/Furto'),
            ('apreendido', 'Apreendido'),
        ],
        default='ativo'
    )
    ultima_posicao_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ultima_posicao_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ultima_atualizacao = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Viatura"
        verbose_name_plural = "Viaturas"
    
    def __str__(self):
        return f"{self.placa} - {self.modelo}"


class RegistroMonitoramento(models.Model):
    """
    Model representing vehicle monitoring records.
    """
    viatura = models.ForeignKey(Viatura, on_delete=models.CASCADE, related_name='registros_monitoramento')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    velocidade = models.IntegerField(null=True, blank=True)
    direcao = models.CharField(max_length=10, blank=True)
    data_registro = models.DateTimeField()
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Registro de Monitoramento"
        verbose_name_plural = "Registros de Monitoramento"
    
    def __str__(self):
        return f"{self.viatura.placa} - {self.data_registro}"