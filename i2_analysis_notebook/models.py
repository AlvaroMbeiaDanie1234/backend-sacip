from django.db import models
from users.models import User


class NotebookAnalise(models.Model):
    """
    Model representing analysis notebooks in the I2 system.
    """
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    conteudo = models.TextField()  # JSON representation of the notebook
    versao = models.CharField(max_length=20, default='1.0')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_ultima_edicao = models.DateTimeField(auto_now=True)
    compartilhado_com = models.ManyToManyField(User, related_name='notebooks_compartilhados', blank=True)
    publico = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Notebook de Análise"
        verbose_name_plural = "Notebooks de Análise"
    
    def __str__(self):
        return self.titulo


class EntidadeAnalise(models.Model):
    """
    Model representing entities analyzed in notebooks.
    """
    notebook = models.ForeignKey(NotebookAnalise, on_delete=models.CASCADE, related_name='entidades')
    nome = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=30,
        choices=[
            ('pessoa', 'Pessoa'),
            ('organizacao', 'Organização'),
            ('local', 'Local'),
            ('evento', 'Evento'),
            ('outro', 'Outro'),
        ]
    )
    dados = models.TextField()  # JSON with entity data
    coordenada_x = models.FloatField(null=True, blank=True)
    coordenada_y = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Entidade de Análise"
        verbose_name_plural = "Entidades de Análise"
    
    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class ConexaoAnalise(models.Model):
    """
    Model representing connections between entities in analysis notebooks.
    """
    notebook = models.ForeignKey(NotebookAnalise, on_delete=models.CASCADE, related_name='conexoes')
    origem = models.ForeignKey(EntidadeAnalise, on_delete=models.CASCADE, related_name='conexoes_origem')
    destino = models.ForeignKey(EntidadeAnalise, on_delete=models.CASCADE, related_name='conexoes_destino')
    tipo_conexao = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)
    peso = models.FloatField(default=1.0)  # Connection strength
    
    class Meta:
        verbose_name = "Conexão de Análise"
        verbose_name_plural = "Conexões de Análise"
        unique_together = ('origem', 'destino', 'tipo_conexao')
    
    def __str__(self):
        return f"{self.origem.nome} -> {self.destino.nome} ({self.tipo_conexao})"