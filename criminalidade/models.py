from django.db import models
from users.models import User


class TipoCrime(models.Model):
    """
    Model representing crime types.
    """
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    codigo_penal = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Tipo de Crime"
        verbose_name_plural = "Tipos de Crimes"
    
    def __str__(self):
        return self.nome


class Ocorrencia(models.Model):
    """
    Model representing crime occurrences.
    """
    tipo_crime = models.ForeignKey(TipoCrime, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_ocorrencia = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    endereco = models.TextField()
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    data_registro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('registrado', 'Registrado'),
            ('investigando', 'Em Investigação'),
            ('resolvido', 'Resolvido'),
            ('arquivado', 'Arquivado'),
        ],
        default='registrado'
    )
    nivel_gravidade = models.IntegerField(default=1)  # 1-5 scale
    
    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
    
    def __str__(self):
        return f"{self.tipo_crime.nome} - {self.data_ocorrencia.strftime('%d/%m/%Y')}"


class Envolvido(models.Model):
    """
    Model representing people involved in crimes (victims, suspects, witnesses).
    """
    TIPO_ENVOLVIMENTO_CHOICES = [
        ('vitima', 'Vítima'),
        ('suspeito', 'Suspeito'),
        ('testemunha', 'Testemunha'),
        ('outro', 'Outro'),
    ]
    
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name='envolvidos')
    nome = models.CharField(max_length=200)
    tipo_envolvimento = models.CharField(max_length=20, choices=TIPO_ENVOLVIMENTO_CHOICES)
    idade = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    contato = models.CharField(max_length=50, blank=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Envolvido"
        verbose_name_plural = "Envolvidos"
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_envolvimento_display()})"