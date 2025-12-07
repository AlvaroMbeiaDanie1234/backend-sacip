from django.db import models
from users.models import User


class Documento(models.Model):
    """
    Model representing documents in the system.
    """
    TIPO_DOCUMENTO_CHOICES = [
        ('rg', 'RG'),
        ('cpf', 'CPF'),
        ('passaporte', 'Passaporte'),
        ('cnh', 'CNH'),
        ('certidao', 'Certidão'),
        ('outro', 'Outro'),
    ]
    
    numero = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    nome_titular = models.CharField(max_length=200)
    data_emissao = models.DateField(null=True, blank=True)
    orgao_emissor = models.CharField(max_length=100, blank=True)
    arquivo = models.FileField(upload_to='documentos/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.numero}"