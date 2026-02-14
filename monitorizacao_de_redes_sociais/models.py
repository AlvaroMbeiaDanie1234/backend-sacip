from django.db import models
from users.models import User


class LinkRedeSocialAlvo(models.Model):
    """
    Associação de um perfil/link de rede social (ex: encontrado via Sherlock) a um alvo sob investigação.
    """
    alvo_id = models.IntegerField(db_index=True)  # FK to alvos_sob_investigacao.AlvoInvestigacao (cross-app)
    nome_site = models.CharField(max_length=150)
    url_perfil = models.URLField(max_length=500)
    data_associacao = models.DateTimeField(auto_now_add=True)
    associado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Link Rede Social (Alvo)"
        verbose_name_plural = "Links Redes Sociais (Alvos)"
        ordering = ["-data_associacao"]
        unique_together = [["alvo_id", "nome_site"]]  # evita duplicar o mesmo site por alvo

    def __str__(self):
        return f"Alvo {self.alvo_id} — {self.nome_site}"


class PerfilRedeSocial(models.Model):
    """
    Model representing social media profiles being monitored.
    """
    nome_usuario = models.CharField(max_length=100)
    plataforma = models.CharField(
        max_length=20,
        choices=[
            ('facebook', 'Facebook'),
            ('twitter', 'Twitter/X'),
            ('instagram', 'Instagram'),
            ('linkedin', 'LinkedIn'),
            ('tiktok', 'TikTok'),
            ('youtube', 'YouTube'),
        ]
    )
    url_perfil = models.URLField()
    nome_completo = models.CharField(max_length=200, blank=True)
    biografia = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)
    monitorado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Perfil de Rede Social"
        verbose_name_plural = "Perfis de Redes Sociais"
    
    def __str__(self):
        return f"{self.nome_usuario} - {self.plataforma}"


class Postagem(models.Model):
    """
    Model representing social media posts.
    """
    perfil = models.ForeignKey(PerfilRedeSocial, on_delete=models.CASCADE, related_name='postagens')
    post_id = models.CharField(max_length=100)  # ID from the platform
    conteudo = models.TextField()
    data_postagem = models.DateTimeField()
    curtidas = models.IntegerField(default=0)
    compartilhamentos = models.IntegerField(default=0)
    comentarios = models.IntegerField(default=0)
    url_postagem = models.URLField()
    marcadores = models.TextField(blank=True)  # Tags, mentions, etc.
    relevancia = models.IntegerField(default=1)  # 1-10 scale
    data_coleta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"
    
    def __str__(self):
        return f"Post de {self.perfil.nome_usuario} em {self.data_postagem}"


class AlertaMonitoramento(models.Model):
    """
    Model representing monitoring alerts for keywords/ phrases
    """
    termo_busca = models.CharField(max_length=200, help_text="Termo ou frase a ser monitorada")
    descricao = models.TextField(blank=True, help_text="Descrição opcional do alerta")
    ativo = models.BooleanField(default=True, help_text="Indica se o alerta está ativo")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_verificacao = models.DateTimeField(null=True, blank=True, help_text="Última vez que o termo foi verificado")
    monitorado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Alerta de Monitoramento"
        verbose_name_plural = "Alertas de Monitoramento"
    
    def __str__(self):
        return f"Alerta: {self.termo_busca}"