from django.db import models
from users.models import User, Role


class ConfiguracaoSistema(models.Model):
    """
    Model representing system-wide configurations.
    """
    chave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descricao = models.TextField(blank=True)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('string', 'Texto'),
            ('integer', 'Número Inteiro'),
            ('float', 'Número Decimal'),
            ('boolean', 'Booleano'),
            ('json', 'JSON'),
        ],
        default='string'
    )
    visivel_roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name='configuracoes_visiveis',
        help_text="Roles que podem visualizar esta configuração"
    )
    editavel_roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name='configuracoes_editaveis',
        help_text="Roles que podem editar esta configuração"
    )
    
    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"
    
    def __str__(self):
        return self.chave


class Auditoria(models.Model):
    """
    Model representing audit logs for system actions.
    """
    ACAO_CHOICES = [
        ('criacao', 'Criação'),
        ('atualizacao', 'Atualização'),
        ('exclusao', 'Exclusão'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('exportacao', 'Exportação'),
        ('outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    modelo = models.CharField(max_length=100)
    objeto_id = models.PositiveIntegerField()
    descricao = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Registro de Auditoria"
        verbose_name_plural = "Registros de Auditoria"
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.usuario} - {self.acao} {self.modelo} em {self.data_hora}"


class Notificacao(models.Model):
    """
    Model representing system notifications.
    """
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    destinatarios = models.ManyToManyField(User, related_name='notificacoes', blank=True)
    lida_por = models.ManyToManyField(User, related_name='notificacoes_lidas', blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return self.titulo


class PermissaoCustomizada(models.Model):
    """
    Model representing custom permissions for specific actions.
    """
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    roles_autorizadas = models.ManyToManyField(
        Role,
        related_name='permissoes_customizadas',
        blank=True
    )
    
    class Meta:
        verbose_name = "Permissão Customizada"
        verbose_name_plural = "Permissões Customizadas"
    
    def __str__(self):
        return self.nome