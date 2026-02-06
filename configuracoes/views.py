from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ConfiguracaoSistema, ConfiguracaoUsuario, Configuracao, TermoOfensivo
from .serializers import (
    ConfiguracaoSistemaSerializer, 
    ConfiguracaoUsuarioSerializer, 
    ConfiguracaoSerializer, 
    TermoOfensivoSerializer
)
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

User = get_user_model()

class ConfiguracaoSistemaListView(generics.ListCreateAPIView):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConfiguracaoSistemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfiguracaoSistema.objects.all()
    serializer_class = ConfiguracaoSistemaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConfiguracaoUsuarioListView(generics.ListCreateAPIView):
    queryset = ConfiguracaoUsuario.objects.all()
    serializer_class = ConfiguracaoUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only configurations for the current user
        return ConfiguracaoUsuario.objects.filter(usuario=self.request.user)

class ConfiguracaoUsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConfiguracaoUsuario.objects.all()
    serializer_class = ConfiguracaoUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only configurations for the current user
        return ConfiguracaoUsuario.objects.filter(usuario=self.request.user)

class ConfiguracaoListView(generics.ListCreateAPIView):
    queryset = Configuracao.objects.all()
    serializer_class = ConfiguracaoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConfiguracaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Configuracao.objects.all()
    serializer_class = ConfiguracaoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Offensive Terms Dictionary Views
class TermoOfensivoListView(generics.ListCreateAPIView):
    queryset = TermoOfensivo.objects.all()
    serializer_class = TermoOfensivoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class TermoOfensivoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TermoOfensivo.objects.all()
    serializer_class = TermoOfensivoSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def get_termos_ofensivos_public(request):
    """
    Public endpoint to get active offensive terms
    """
    try:
        termos = TermoOfensivo.objects.filter(ativo=True).values_list('termo', flat=True)
        return Response(list(termos), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_termos_ofensivos_by_severity(request):
    """
    Get offensive terms grouped by severity level
    """
    try:
        termos = TermoOfensivo.objects.filter(ativo=True)
        result = {}
        for termo in termos:
            severity = str(termo.nivel_severidade)
            if severity not in result:
                result[severity] = []
            result[severity].append({
                'id': termo.id,
                'termo': termo.termo,
                'descricao': termo.descricao
            })
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Temporary mock endpoints for testing when database isn't ready
@api_view(['GET'])
def get_termos_ofensivos_mock(request):
    """
    Mock endpoint for testing - returns sample offensive terms
    """
    mock_terms = [
        {
            'id': 1,
            'termo': 'filho da puta',
            'descricao': 'Expressão vulgar e ofensiva',
            'nivel_severidade': 8,
            'ativo': True,
            'criado_em': '2024-01-01T00:00:00Z',
            'atualizado_em': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'termo': 'roubar',
            'descricao': 'Ato de tirar algo sem permissão',
            'nivel_severidade': 6,
            'ativo': True,
            'criado_em': '2024-01-01T00:00:00Z',
            'atualizado_em': '2024-01-01T00:00:00Z'
        },
        {
            'id': 3,
            'termo': 'matar',
            'descricao': 'Ato de causar morte',
            'nivel_severidade': 10,
            'ativo': True,
            'criado_em': '2024-01-01T00:00:00Z',
            'atualizado_em': '2024-01-01T00:00:00Z'
        },
        {
            'id': 4,
            'termo': 'mpla',
            'descricao': 'Termo político potencialmente ofensivo',
            'nivel_severidade': 5,
            'ativo': True,
            'criado_em': '2024-01-01T00:00:00Z',
            'atualizado_em': '2024-01-01T00:00:00Z'
        }
    ]
    return Response(mock_terms, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_termo_ofensivo_mock(request):
    """
    Mock endpoint for creating offensive terms
    """
    return Response({'error': 'Database not ready - mock endpoint'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_termo_ofensivo_mock(request, pk):
    """
    Mock endpoint for updating offensive terms
    """
    return Response({'error': 'Database not ready - mock endpoint'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_termo_ofensivo_mock(request, pk):
    """
    Mock endpoint for deleting offensive terms
    """
    return Response({'error': 'Database not ready - mock endpoint'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)