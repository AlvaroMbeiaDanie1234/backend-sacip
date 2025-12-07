from django.db import models
from users.models import User


class ChamadaSOS(models.Model):
    """
    Model representing SOS calls in the system.
    """
    STATUS_CHOICES = [
        ('recebida', 'Recebida'),
        ('em_atendimento', 'Em Atendimento'),
        ('atendida', 'Atendida'),
        ('encerrada', 'Encerrada'),
    ]
    
    numero_origem = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    endereco = models.TextField(blank=True)
    descricao = models.TextField()
    data_hora_chamada = models.DateTimeField(auto_now_add=True)
    data_hora_atendimento = models.DateTimeField(null=True, blank=True)
    data_hora_encerramento = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebida')
    operador = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='chamadas_atendidas'
    )
    duracao_segundos = models.IntegerField(null=True, blank=True)
    prioridade = models.IntegerField(default=1)  # 1-5 scale
    
    class Meta:
        verbose_name = "Chamada SOS"
        verbose_name_plural = "Chamadas SOS"
    
    def __str__(self):
        return f"SOS {self.numero_origem} - {self.data_hora_chamada.strftime('%d/%m/%Y %H:%M')}"


class UnidadePolicial(models.Model):
    """
    Model representing police units available for SOS response.
    """
    nome = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=30,
        choices=[
            ('patrulha', 'Patrulha'),
            ('viatura', 'Viatura'),
            ('helicoptero', 'Helicóptero'),
            ('base', 'Base Policial'),
        ]
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    disponivel = models.BooleanField(default=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    contato_radio = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Unidade Policial"
        verbose_name_plural = "Unidades Policiais"
    
    def __str__(self):
        return f"{self.nome} ({self.tipo})"