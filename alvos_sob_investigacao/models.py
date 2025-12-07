from django.db import models
from users.models import User


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
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Alvo sob Investigação"
        verbose_name_plural = "Alvos sob Investigação"
    
    def __str__(self):
        return f"{self.nome} {self.apelido} ({self.cpf})"