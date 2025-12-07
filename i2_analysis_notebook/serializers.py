from rest_framework import serializers
from .models import NotebookAnalise, EntidadeAnalise, ConexaoAnalise


class NotebookAnaliseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookAnalise
        fields = '__all__'
        read_only_fields = ('data_criacao', 'data_ultima_edicao', 'criado_por')


class EntidadeAnaliseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntidadeAnalise
        fields = '__all__'


class ConexaoAnaliseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConexaoAnalise
        fields = '__all__'