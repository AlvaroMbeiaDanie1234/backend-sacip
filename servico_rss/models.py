from django.db import models
from users.models import User

class FonteRSS(models.Model):
    """
    Model representing RSS feed sources.
    """
    nome = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)
    adicionado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Fonte RSS"
        verbose_name_plural = "Fontes RSS"
    
    def __str__(self):
        return self.nome

class NoticiaRSS(models.Model):
    """
    Model representing news articles from RSS feeds.
    """
    titulo = models.CharField(max_length=500)
    descricao = models.TextField(blank=True)
    url = models.URLField(unique=True)
    data_publicacao = models.DateTimeField()
    autor = models.CharField(max_length=200, blank=True)
    conteudo = models.TextField(blank=True)
    fonte = models.ForeignKey(FonteRSS, on_delete=models.CASCADE, related_name='noticias')
    data_coleta = models.DateTimeField(auto_now_add=True)
    relevancia = models.IntegerField(default=1)  # 1-10 scale
    
    class Meta:
        verbose_name = "Notícia RSS"
        verbose_name_plural = "Notícias RSS"
        ordering = ['-data_publicacao']
    
    def __str__(self):
        return self.titulo