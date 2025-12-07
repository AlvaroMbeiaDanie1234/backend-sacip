from django.db import models
from users.models import User


class TipoRelatorio(models.Model):
    """
    Model representing report types.
    """
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    template = models.TextField(blank=True)  # Template for generating reports
    
    class Meta:
        verbose_name = "Tipo de Relatório"
        verbose_name_plural = "Tipos de Relatórios"
    
    def __str__(self):
        return self.nome


class Relatorio(models.Model):
    """
    Model representing generated reports.
    """
    titulo = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoRelatorio, on_delete=models.CASCADE)
    conteudo = models.TextField()  # Generated report content
    parametros = models.TextField(blank=True)  # JSON with generation parameters
    data_geracao = models.DateTimeField(auto_now_add=True)
    gerado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    formato = models.CharField(
        max_length=10,
        choices=[
            ('pdf', 'PDF'),
            ('xlsx', 'Excel'),
            ('docx', 'Word'),
            ('html', 'HTML'),
            ('csv', 'CSV'),
        ],
        default='pdf'
    )
    arquivo = models.FileField(upload_to='relatorios/', null=True, blank=True)
    publico = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
    
    def __str__(self):
        return f"{self.titulo} - {self.data_geracao.strftime('%d/%m/%Y')}"


class AgendamentoRelatorio(models.Model):
    """
    Model representing scheduled report generation.
    """
    nome = models.CharField(max_length=100)
    tipo_relatorio = models.ForeignKey(TipoRelatorio, on_delete=models.CASCADE)
    parametros = models.TextField(blank=True)  # JSON with generation parameters
    frequencia = models.CharField(
        max_length=20,
        choices=[
            ('diaria', 'Diária'),
            ('semanal', 'Semanal'),
            ('mensal', 'Mensal'),
            ('anual', 'Anual'),
            ('personalizada', 'Personalizada'),
        ]
    )
    dia_semana = models.IntegerField(
        null=True, 
        blank=True,
        choices=[(i, day) for i, day in enumerate(['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'])]
    )
    dia_mes = models.IntegerField(null=True, blank=True)  # 1-31
    hora_execucao = models.TimeField()
    ativo = models.BooleanField(default=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_execucao = models.DateTimeField(null=True, blank=True)
    proxima_execucao = models.DateTimeField()
    
    class Meta:
        verbose_name = "Agendamento de Relatório"
        verbose_name_plural = "Agendamentos de Relatórios"
    
    def __str__(self):
        return f"{self.nome} - {self.frequencia}"