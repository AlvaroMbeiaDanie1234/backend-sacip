from django.db import models
from users.models import User


class FonteDados(models.Model):
    """
    Model representing data sources for cross-referencing.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(
        max_length=30,
        choices=[
            ('banco_dados', 'Banco de Dados'),
            ('api', 'API'),
            ('arquivo', 'Arquivo'),
            ('web_scraping', 'Web Scraping'),
            ('outro', 'Outro'),
        ]
    )
    url_conexao = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Fonte de Dados"
        verbose_name_plural = "Fontes de Dados"
    
    def __str__(self):
        return self.nome


class Cruzamento(models.Model):
    """
    Model representing data cross-referencing operations.
    """
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    fontes = models.ManyToManyField(FonteDados, related_name='cruzamentos')
    parametros = models.TextField(blank=True)  # JSON with search parameters
    resultado = models.TextField(blank=True)   # JSON with cross-reference results
    data_execucao = models.DateTimeField(null=True, blank=True)
    executado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('executando', 'Executando'),
            ('concluido', 'Concluído'),
            ('erro', 'Erro'),
        ],
        default='pendente'
    )
    tempo_execucao_segundos = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Cruzamento de Dados"
        verbose_name_plural = "Cruzamentos de Dados"
    
    def __str__(self):
        return self.nome


class Relacionamento(models.Model):
    """
    Model representing relationships found between entities during cross-referencing.
    """
    TIPO_RELACIONAMENTO_CHOICES = [
        ('familiar', 'Familiar'),
        ('financeiro', 'Financeiro'),
        ('profissional', 'Profissional'),
        ('social', 'Social'),
        ('criminal', 'Criminal'),
        ('outro', 'Outro'),
    ]
    
    cruzamento = models.ForeignKey(Cruzamento, on_delete=models.CASCADE, related_name='relacionamentos')
    entidade_a = models.CharField(max_length=200)  # Person, company, etc.
    entidade_b = models.CharField(max_length=200)
    tipo_relacionamento = models.CharField(max_length=20, choices=TIPO_RELACIONAMENTO_CHOICES)
    grau_confianca = models.IntegerField(default=1)  # 1-10 scale
    evidencias = models.TextField(blank=True)  # Supporting evidence
    data_descoberta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Relacionamento"
        verbose_name_plural = "Relacionamentos"
    
    def __str__(self):
        return f"{self.entidade_a} -> {self.entidade_b} ({self.get_tipo_relacionamento_display()})"