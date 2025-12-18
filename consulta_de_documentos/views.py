from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Documento
from .serializers import DocumentoSerializer
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

# External API URL for document verification
EXTERNAL_API_URL = 'https://consulta.edgarsingui.ao/consultar'


class DocumentoListCreateView(generics.ListCreateAPIView):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class DocumentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access for document verification
def verificar_documento(request):
    """
    Verify a document by number using the external API
    """
    numero = request.GET.get('numero')
    
    if not numero:
        return Response(
            {'error': True, 'message': 'Número de consulta é obrigatório'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Make request to external API
        api_url = f"{EXTERNAL_API_URL}/{numero}"
        logger.info(f"Consultando API externa: {api_url}")
        
        api_response = requests.get(api_url, timeout=30)
        
        # Log the response for debugging
        logger.info(f"Resposta da API externa - Status: {api_response.status_code}")
        logger.info(f"Conteúdo da resposta: {api_response.text}")
        
        if api_response.status_code == 200:
            return Response(api_response.json())
        else:
            # Handle non-200 responses
            return Response(
                {'error': True, 'message': f'Erro na API externa: {api_response.status_code}'}, 
                status=api_response.status_code
            )
            
    except requests.exceptions.Timeout:
        logger.error('Timeout ao consultar API externa')
        return Response(
            {'error': True, 'message': 'Tempo limite excedido ao consultar serviço externo'}, 
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        logger.error('Erro de conexão ao consultar API externa')
        return Response(
            {'error': True, 'message': 'Erro de conexão ao consultar serviço externo'}, 
            status=status.HTTP_502_BAD_GATEWAY
        )
    except Exception as e:
        logger.error(f'Erro ao consultar API externa: {str(e)}')
        return Response(
            {'error': True, 'message': 'Erro interno ao processar a consulta'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )