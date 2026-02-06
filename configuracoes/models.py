from django.db import models
from users.models import User

class Configuracao(models.Model):
    """
    Model for general system configurations
    """
    chave = models.CharField(max_length=255, unique=True)
    valor = models.TextField()
    descricao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        ordering = ['chave']

    def __str__(self):
        return f"{self.chave}: {self.valor[:50]}"


class TermoOfensivo(models.Model):
    """
    Model for offensive terms dictionary
    """
    termo = models.CharField(max_length=255, unique=True, help_text="Termo ofensivo a ser monitorado")
    descricao = models.TextField(blank=True, help_text="Descrição opcional do termo")
    nivel_severidade = models.IntegerField(default=1, help_text="Nível de severidade (1-10)")
    ativo = models.BooleanField(default=True, help_text="Indica se o termo está ativo para monitoramento")
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='termos_criados')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Termo Ofensivo'
        verbose_name_plural = 'Termos Ofensivos'
        ordering = ['termo']

    def __str__(self):
        return f"{self.termo} (Severidade: {self.nivel_severidade})"


class ConfiguracaoSistema(models.Model):
    """
    Model for system-wide configurations
    """
    CHAVES_PERMITIDAS = [
        ('EMAIL_HOST', 'Host do servidor de e-mail'),
        ('EMAIL_PORT', 'Porta do servidor de e-mail'),
        ('EMAIL_USE_TLS', 'Usar TLS para e-mail'),
        ('EMAIL_HOST_USER', 'Usuário do servidor de e-mail'),
        ('EMAIL_HOST_PASSWORD', 'Senha do servidor de e-mail'),
        ('MAX_FILE_UPLOAD_SIZE', 'Tamanho máximo de upload de arquivo (bytes)'),
        ('ALLOWED_FILE_EXTENSIONS', 'Extensões de arquivo permitidas'),
        ('SESSION_TIMEOUT', 'Tempo limite da sessão (segundos)'),
        ('MAX_LOGIN_ATTEMPTS', 'Número máximo de tentativas de login'),
        ('LOCKOUT_TIME', 'Tempo de bloqueio após tentativas falhas (segundos)'),
        ('LOG_RETENTION_DAYS', 'Dias de retenção de logs'),
        ('AUDIT_LOG_ENABLED', 'Registro de auditoria habilitado'),
        ('BACKUP_ENABLED', 'Backup automático habilitado'),
        ('BACKUP_SCHEDULE', 'Agendamento de backup'),
        ('NOTIFICATION_EMAIL_ENABLED', 'Notificações por e-mail habilitadas'),
        ('NOTIFICATION_SMS_ENABLED', 'Notificações por SMS habilitadas'),
        ('SECURITY_LOGGING_ENABLED', 'Registro de segurança habilitado'),
        ('OFFENSIVE_TERMS_MONITORING', 'Monitoramento de termos ofensivos'),
    ]
    
    chave = models.CharField(max_length=255, unique=True, choices=CHAVES_PERMITIDAS)
    valor = models.TextField(help_text="Valor da configuração")
    descricao = models.TextField(blank=True, help_text="Descrição da configuração")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
        ordering = ['chave']

    def __str__(self):
        return f"{self.chave}: {self.valor[:50]}"


class ConfiguracaoUsuario(models.Model):
    """
    Model for user-specific configurations
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='configuracoes_usuario')
    chave = models.CharField(max_length=255, help_text="Chave da configuração específica do usuário")
    valor = models.TextField(help_text="Valor da configuração")
    descricao = models.TextField(blank=True, help_text="Descrição da configuração")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Usuário'
        verbose_name_plural = 'Configurações do Usuário'
        unique_together = ('usuario', 'chave')
        ordering = ['usuario', 'chave']

    def __str__(self):
        return f"{self.usuario.username} - {self.chave}: {self.valor[:30]}"