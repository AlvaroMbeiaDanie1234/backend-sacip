from django.db import models
from users.models import User
from facial_recognition.models import Suspect


class AlvoInvestigacao(models.Model):
    """
    Model representing investigation targets in the system.
    """
    nome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=100, blank=True)
    cpf = models.CharField(max_length=14, unique=True)  # Brazilian CPF format
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ativo', 'Ativo'),
            ('inativo', 'Inativo'),
            ('concluido', 'Concluído'),
        ],
        default='ativo'
    )
    nivel_prioridade = models.IntegerField(default=1)  # 1-5 scale
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    investigador_responsavel = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alvos_investigacao'
    )
#    suspect = models.ForeignKey(
#        Suspect,
#        on_delete=models.SET_NULL,
#        null=True,
#        blank=True,
#        related_name='alvos_investigacao'
#    )
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Alvo sob Investigação"
        verbose_name_plural = "Alvos sob Investigação"
    
    def __str__(self):
        return f"{self.nome} {self.apelido} ({self.cpf})"


class CommunicationHistory(models.Model):
    """
    Model to store communication history (SMS/Email) sent to targets
    """
    COMMUNICATION_TYPES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
    ]
    
    target = models.ForeignKey(
        AlvoInvestigacao,
        on_delete=models.CASCADE,
        related_name='communications'
    )
    communication_type = models.CharField(
        max_length=10,
        choices=COMMUNICATION_TYPES
    )
    recipient = models.CharField(max_length=255)  # Phone number or email address
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_communications'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('sent', 'Sent'),
            ('failed', 'Failed'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
        ],
        default='sent'
    )
    response = models.TextField(blank=True)  # For storing delivery receipts or responses
    external_reference = models.CharField(max_length=255, blank=True)  # External API reference ID
    
    class Meta:
        verbose_name = "Histórico de Comunicação"
        verbose_name_plural = "Históricos de Comunicação"
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.communication_type.upper()} para {self.recipient} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"


class AntecedenteCriminal(models.Model):
    """
    Model to store criminal records for a target.
    """
    STATUS_CHOICES = [
        ('suspeito', 'Suspeito'),
        ('acusado', 'Acusado'),
        ('condenado', 'Condenado'),
        ('arquivado', 'Arquivado'),
        ('cumprido', 'Pena Cumprida'),
    ]
    
    alvo = models.ForeignKey(
        AlvoInvestigacao,
        on_delete=models.CASCADE,
        related_name='antecedentes_criminais'
    )
    tipo_crime = models.CharField(max_length=100)
    data_crime = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='suspeito')
    pena = models.CharField(max_length=100, blank=True)
    local_crime = models.CharField(max_length=255, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Antecedente Criminal"
        verbose_name_plural = "Antecedentes Criminais"
        ordering = ['-data_crime']
    
    def __str__(self):
        return f"{self.tipo_crime} - {self.alvo.nome} ({self.status})"


class OSINTEntrada(models.Model):
    """
    Model to store OSINT data (text or images) associated with a target.
    """
    TYPE_CHOICES = [
        ('text', 'Texto'),
        ('image', 'Imagem'),
    ]
    
    alvo = models.ForeignKey(
        AlvoInvestigacao,
        on_delete=models.CASCADE,
        related_name='osint_entries'
    )
    tipo = models.CharField(max_length=10, choices=TYPE_CHOICES)
    conteudo = models.TextField()  # Can be text content or image URL
    titulo = models.CharField(max_length=255, blank=True)
    fonte = models.CharField(max_length=255, blank=True)
    data_associacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Entrada OSINT"
        verbose_name_plural = "Entradas OSINT"
        ordering = ['-data_associacao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.alvo.nome} - {self.data_associacao}"