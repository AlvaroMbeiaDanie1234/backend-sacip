"""
Spyware API Views for Information Gathering
Educational/Study Purposes Only
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
import json
from .spyware_utils_safe import create_spyware_session, decrypt_collected_data
from .models import InformacaoSuspeita
from facial_recognition.models import Suspect
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def start_surveillance(request):
    """
    Start a surveillance session for information gathering
    """
    try:
        suspect_id = request.data.get('suspect_id')
        operation_name = request.data.get('operation_name', 'Surveillance Operation')
        duration = request.data.get('duration', 300)  # Default 5 minutes
        
        # Validate suspect exists if provided
        suspect = None
        if suspect_id:
            try:
                suspect = Suspect.objects.get(id=suspect_id)
            except Suspect.DoesNotExist:
                return Response(
                    {'error': 'Suspect not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Start surveillance session
        session_data = create_spyware_session(
            suspect_id=suspect_id,
            operation_name=operation_name
        )
        
        # Create information record
        informacao_data = {
            'titulo': f"Surveillance: {operation_name}",
            'descricao': f"Surveillance operation: {operation_name}",
            'detalhes': json.dumps(session_data),
            'ativo': True,
            'criado_por_id': 1  # Default user ID
        }
        
        if suspect:
            informacao_data['suspect'] = suspect.id
            
        # Save to database
        informacao = InformacaoSuspeita.objects.create(**informacao_data)
        
        return Response({
            'message': 'Surveillance session started successfully',
            'session_id': session_data['session_id'],
            'informacao_id': informacao.id,
            'operation_name': operation_name,
            'suspect_id': suspect_id,
            'duration': duration
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error starting surveillance: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def decrypt_session_data(request):
    """
    Decrypt data collected from a surveillance session
    """
    try:
        session_id = request.data.get('session_id')
        decryption_key = request.data.get('decryption_key')
        
        if not session_id:
            return Response(
                {'error': 'Session ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Perform decryption
        decryption_result = decrypt_collected_data(
            session_id, 
            decryption_key.encode() if decryption_key else None
        )
        
        return Response({
            'message': 'Data decryption completed',
            'result': decryption_result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error decrypting data: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_session_status(request, session_id):
    """
    Get status of a surveillance session
    """
    try:
        # Try to find information record for this session
        try:
            informacao = InformacaoSuspeita.objects.get(
                titulo__icontains='surveillance',
                detalhes__contains=session_id
            )
            
            # Parse session data
            detalhes = json.loads(informacao.detalhes) if informacao.detalhes else {}
            
            return Response({
                'session_id': session_id,
                'status': 'ativo' if informacao.ativo else 'inativo',
                'operation_name': detalhes.get('operation_name', 'Unknown'),
                'suspect_id': detalhes.get('suspect_id'),
                'created_at': informacao.data_criacao,
                'created_by': 'System'
            })
            
        except InformacaoSuspeita.DoesNotExist:
            return Response(
                {'error': 'Session not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.error(f"Error getting session status: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def list_surveillance_operations(request):
    """
    List all surveillance operations
    """
    try:
        # Get all spyware surveillance operations
        operations = InformacaoSuspeita.objects.filter(
            titulo__icontains='surveillance'
        ).order_by('-data_criacao')
        
        operations_data = []
        for op in operations:
            detalhes = json.loads(op.detalhes) if op.detalhes else {}
            operations_data.append({
                'id': op.id,
                'session_id': detalhes.get('session_id', 'Unknown'),
                'operation_name': detalhes.get('operation_name', 'Unknown'),
                'suspect_id': detalhes.get('suspect_id'),
                'status': 'ativo' if op.ativo else 'inativo',
                'created_at': op.data_criacao,
                'created_by': 'System'
            })
        
        return Response({
            'operations': operations_data,
            'count': len(operations_data)
        })
        
    except Exception as e:
        logger.error(f"Error listing operations: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def stop_surveillance(request, session_id):
    """
    Stop an active surveillance session
    """
    try:
        # Find the operation record
        try:
            informacao = InformacaoSuspeita.objects.get(
                titulo__icontains='surveillance',
                detalhes__contains=session_id,
                ativo=True
            )
            
            # Update status to completed
            informacao.ativo = False
            informacao.save()
            
            return Response({
                'message': 'Surveillance session stopped successfully',
                'session_id': session_id,
                'status': 'completed'
            })
            
        except InformacaoSuspeita.DoesNotExist:
            return Response(
                {'error': 'Active session not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.error(f"Error stopping surveillance: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )