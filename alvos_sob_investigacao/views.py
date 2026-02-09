import logging
import uuid
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import AlvoInvestigacao
from .serializers import AlvoInvestigacaoSerializer
from .firebase_utils import get_firebase_data, get_firebase_record, search_firebase_data, get_multiple_firebase_paths
from .firestore_utils import get_firestore_collection, get_firestore_document, query_firestore_collection
from .models import CommunicationHistory
from .serializers import CommunicationHistorySerializer, CommunicationHistoryListSerializer


class FirebaseDataView(APIView):
    """
    View to retrieve data from Firebase Realtime Database.
    Provides endpoints to fetch data from Firebase and return it to the frontend.
    """
    permission_classes = []  # Removed authentication requirement
    
    def get(self, request):
        """
        Retrieve data from Firebase based on the path provided in query parameters.
        Usage: GET /firebase-data/?path=/suspects
        """
        path = request.query_params.get('path', '/')
        if not path:
            path = '/'
        
        try:
            data = get_firebase_data(path)
            return Response({
                'success': True,
                'path': path,
                'data': data
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def post(self, request):
        """
        Perform various operations on Firebase data based on the action specified.
        Actions supported:
        - 'get': Get data from a specific path
        - 'search': Search data with query parameters
        - 'get_multiple': Get data from multiple paths
        """
        action = request.data.get('action', 'get')
        path = request.data.get('path', '/')
        
        try:
            if action == 'get':
                if 'record_id' in request.data:
                    record_id = request.data.get('record_id')
                    data = get_firebase_record(path, record_id)
                    return Response({
                        'success': True,
                        'action': action,
                        'path': f"{path}/{record_id}",
                        'data': data
                    })
                else:
                    data = get_firebase_data(path)
                    return Response({
                        'success': True,
                        'action': action,
                        'path': path,
                        'data': data
                    })
            
            elif action == 'search':
                query_params = request.data.get('query_params', {})
                data = search_firebase_data(path, query_params)
                return Response({
                    'success': True,
                    'action': action,
                    'path': path,
                    'query_params': query_params,
                    'data': data
                })
            
            elif action == 'get_multiple':
                paths = request.data.get('paths', [])
                if not paths:
                    return Response({
                        'success': False,
                        'error': 'Paths list is required for get_multiple action'
                    }, status=400)
                
                data = get_multiple_firebase_paths(paths)
                return Response({
                    'success': True,
                    'action': action,
                    'paths': paths,
                    'data': data
                })
            
            else:
                return Response({
                    'success': False,
                    'error': f"Unsupported action: {action}. Supported actions: get, search, get_multiple"
                }, status=400)
        
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)


class AlvoInvestigacaoListCreateView(generics.ListCreateAPIView):
    queryset = AlvoInvestigacao.objects.all()
    serializer_class = AlvoInvestigacaoSerializer
    permission_classes = []  # Removed authentication requirement


class AlvoInvestigacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlvoInvestigacao.objects.all()
    serializer_class = AlvoInvestigacaoSerializer
    permission_classes = []  # Removed authentication requirement


from .email_utils import send_target_investigation_email, send_test_email
from .sms_utils import send_sms_message, send_test_sms

class AlvoInvestigacaoUpdateDocumentoView(APIView):
    permission_classes = []  # Allow unauthenticated access
    
    def post(self, request, pk):
        try:
            # Get the target instance
            instance = AlvoInvestigacao.objects.get(pk=pk)
            
            # Check if the numero_identificacao field is in the request data
            if isinstance(request.data, dict):
                numero_identificacao = request.data.get('numero_identificacao')
            else:
                # If request.data is not a dict, try to parse it differently
                numero_identificacao = getattr(request.data, 'get', lambda x, default=None: default)('numero_identificacao')
            
            if numero_identificacao is None:
                return Response({'error': 'Apenas o campo numero_identificacao pode ser atualizado'}, status=400)
            
            # Check if this CPF already exists for another target
            existing_target_with_cpf = AlvoInvestigacao.objects.filter(cpf=numero_identificacao).exclude(pk=pk).first()
            if existing_target_with_cpf:
                return Response({'error': f'O Número de identidade {numero_identificacao} já está associado a outro alvo (ID: {existing_target_with_cpf.id})'}, status=400)
            
            # Update the cpf field (numero_identificacao maps to cpf in the model)
            instance.cpf = numero_identificacao
            instance.save(update_fields=['cpf'])
            
            # Return the updated instance
            serializer = AlvoInvestigacaoSerializer(instance)
            return Response(serializer.data)
        
        except AlvoInvestigacao.DoesNotExist:
            return Response({'error': 'Target not found'}, status=404)
        except Exception as e:
            # Log the error for debugging
            import logging
            logging.exception(f"Error updating target {pk}: {str(e)}")
            return Response({'error': str(e)}, status=500)


class SendTargetSmsView(APIView):
    permission_classes = []  # Removed authentication requirement
    
    def post(self, request, pk):
        try:
            # Get the target instance
            target = AlvoInvestigacao.objects.get(pk=pk)
            
            # Get recipient phone number, message and subject from request
            recipient_phone = request.data.get('recipient_phone')
            message_body = request.data.get('message', '')
            subject = request.data.get('subject', '')
            
            # If no phone number provided in request, try to get it from the target record
            if not recipient_phone:
                recipient_phone = getattr(target, 'telefone', None)
            
            if not recipient_phone:
                return Response({'error': 'Recipient phone number is required'}, status=400)
            
            # Create structured SMS message with target information if no custom message provided
            if not message_body.strip():
                # Create a default structured message similar to email
                message_body = self._create_structured_sms_message(target, subject)
            elif subject and subject != f"Informações sobre {target.nome}":
                # If there's a subject and it's not the default, prepend it to the message
                message_body = f"{subject}\n{message_body}"
            
            # Send SMS about the target
            success, result = send_sms_message(recipient_phone, message_body)
            
            # Save communication history if the model exists in the database
            history_id = None
            try:
                communication_history = CommunicationHistory.objects.create(
                    target=target,
                    communication_type='sms',
                    recipient=recipient_phone,
                    subject=subject,
                    message=message_body,
                    status='sent' if success else 'failed',
                    response=str(result) if result else ''
                )
                history_id = communication_history.id
            except Exception as db_error:
                # If the CommunicationHistory table doesn't exist, log and continue
                logging.warning(f"Could not save communication history: {str(db_error)}")
            
            if success:
                response_data = {'message': f'SMS sent successfully to {recipient_phone}'}
                if history_id:
                    response_data['history_id'] = history_id
                return Response(response_data)
            else:
                response_data = {'error': 'Failed to send SMS', 'details': result}
                if history_id:
                    response_data['history_id'] = history_id
                return Response(response_data, status=500)
        
        except AlvoInvestigacao.DoesNotExist:
            return Response({'error': 'Target not found'}, status=404)
        except Exception as e:
            logging.exception(f"Error sending SMS for target {pk}: {str(e)}")
            return Response({'error': str(e)}, status=500)
    
    def _create_structured_sms_message(self, target, subject=""):
        """
        Creates a structured SMS message with target information, similar to email functionality
        """
        # Use custom subject if provided, otherwise use default
        if not subject:
            subject = f"Informações sobre {target.nome}"
        
        # Create a structured message with key target information
        structured_message = f"""{subject}

Alvo Sob Investigação:
ID: {target.id}
Nome: {target.nome}
Apelido: {target.apelido or 'N/A'}
Nº Identificação: {target.cpf or 'N/A'}
Telefone: {target.telefone or 'N/A'}
Email: {target.email or 'N/A'}
Status: {target.get_status_display()}
Nível Prioridade: {target.nivel_prioridade}

Observações: {target.observacoes or 'N/A'}

Mensagem do Analista: {getattr(target, 'ultima_atualizacao', 'Nenhuma informação adicional')}"""

        # Truncate if message is too long for SMS (most SMS systems have 160 character limit for single message)
        # We'll keep it to a reasonable length for multi-part SMS
        if len(structured_message) > 800:  # Allowing for multi-part SMS
            structured_message = structured_message[:800] + "\n...(mensagem truncada)"
        
        return structured_message


class SendTestSmsView(APIView):
    permission_classes = []  # Removed authentication requirement
    
    def post(self, request):
        try:
            # Send test SMS
            success, result = send_test_sms()
            
            if success:
                return Response({'message': 'Test SMS sent successfully'})
            else:
                return Response({'error': 'Failed to send test SMS', 'details': result}, status=500)
        
        except Exception as e:
            logging.exception(f"Error sending test SMS: {str(e)}")
            return Response({'error': str(e)}, status=500)
from informacoes_suspeitas.models import InformacaoSuspeita
from facial_recognition.models import Suspect

class AddSuspectAsTargetView(APIView):
    permission_classes = []  # Removed authentication requirement
    
    def post(self, request):
        try:
            # Get the suspect ID and data from the request
            suspect_id = request.data.get('suspect_id')
            suspect_data = request.data.get('suspect_data')
            
            logging.info(f"Received request to add suspect as target. suspect_id: {suspect_id}")
            logging.info(f"Request data: {request.data}")
            
            if not suspect_id:
                return Response({'error': 'Suspect ID is required'}, status=400)
            
            # Try to get the suspect from local database first
            try:
                informacao_suspeita = InformacaoSuspeita.objects.get(id=suspect_id)
                logging.info(f"Found InformacaoSuspeita in local database: {informacao_suspeita}")
                suspect = informacao_suspeita.suspect
                
                # Check if suspect exists
                if not suspect:
                    logging.error(f"No suspect associated with InformacaoSuspeita ID {suspect_id}")
                    return Response({'error': 'Suspect not associated with this information'}, status=400)
                
                logging.info(f"Found associated Suspect: {suspect}")
                
                # Use suspect data from database
                full_name = getattr(suspect, 'full_name', 'Nome Desconhecido')
                suspect_nid = getattr(suspect, 'nid', '') or ''
                nickname = getattr(suspect, 'nickname', '') or ''
                dangerous_level = getattr(suspect, 'dangerous_level', '')
                    
            except InformacaoSuspeita.DoesNotExist:
                logging.warning(f"InformacaoSuspeita with ID {suspect_id} not found in local database")
                
                # If suspect_data was provided, use it to create the target
                if suspect_data:
                    logging.info(f"Using provided suspect_data: {suspect_data}")
                    full_name = suspect_data.get('full_name', 'Nome Desconhecido')
                    suspect_nid = suspect_data.get('nid', '') or ''
                    nickname = suspect_data.get('nickname', '') or ''
                    dangerous_level = suspect_data.get('dangerous', '') or suspect_data.get('dangerous_level', '')
                else:
                    logging.error(f"No suspect_data provided and InformacaoSuspeita not found")
                    return Response({
                        'error': 'Suspect information not found in local database. Please provide suspect_data.'
                    }, status=404)
            
            # Create a new investigation target based on the suspect
            alvo_data = {
                'nome': full_name,
                'apelido': nickname,
                'cpf': suspect_nid,  # Use NID field from suspect
                'endereco': '',  # Suspect model doesn't have address field
                'telefone': '',  # Suspect model doesn't have phone field
                'email': '',  # Suspect model doesn't have email field
                'investigador_responsavel': request.user.id if request.user.is_authenticated else None,
                'observacoes': f'Adicionado a partir de suspeito ID: {suspect_id}',
                'status': 'ativo',  # Default status
            }
            
            # If no NID was provided, generate a default one to satisfy unique constraint
            if not suspect_nid:
                alvo_data['cpf'] = f"DEFAULT_{str(uuid.uuid4())[:8]}"
            
            # Map dangerous_level to nivel_prioridade
            if dangerous_level:
                dangerous_level_lower = dangerous_level.lower()
                if 'muito alta' in dangerous_level_lower or 'very high' in dangerous_level_lower:
                    alvo_data['nivel_prioridade'] = 5
                elif 'alta' in dangerous_level_lower or 'high' in dangerous_level_lower:
                    alvo_data['nivel_prioridade'] = 4
                elif 'media' in dangerous_level_lower or 'medium' in dangerous_level_lower or 'média' in dangerous_level_lower:
                    alvo_data['nivel_prioridade'] = 3
                elif 'baixa' in dangerous_level_lower or 'low' in dangerous_level_lower:
                    alvo_data['nivel_prioridade'] = 1
                else:
                    alvo_data['nivel_prioridade'] = 2
            else:
                alvo_data['nivel_prioridade'] = 1  # Default priority level
            
            logging.info(f"Prepared alvo_data: {alvo_data}")
            
            # Create the new target
            serializer = AlvoInvestigacaoSerializer(data=alvo_data)
            if serializer.is_valid():
                target = serializer.save()
                logging.info(f"Successfully created target with ID: {target.id}")
                return Response(serializer.data, status=201)
            else:
                logging.error(f"Serializer validation failed: {serializer.errors}")
                return Response({'error': 'Validation failed', 'details': serializer.errors}, status=400)
                
        except Exception as e:
            logging.exception(f"Error adding suspect as target: {str(e)}")
            return Response({'error': f'Internal server error: {str(e)}'}, status=500)


class SendTargetEmailView(APIView):
    permission_classes = []  # Removed authentication requirement
    
    def post(self, request, pk):
        try:
            # Get the target instance
            target = AlvoInvestigacao.objects.get(pk=pk)
            
            # Get recipient email, subject and message from request
            recipient_email = request.data.get('recipient_email')
            message_body = request.data.get('message', '')
            subject = request.data.get('subject', '')
            
            if not recipient_email:
                return Response({'error': 'Recipient email is required'}, status=400)
            
            # Send email about the target
            success = send_target_investigation_email(target, recipient_email, message_body, subject)
            
            # Save communication history if the model exists in the database
            history_id = None
            try:
                communication_history = CommunicationHistory.objects.create(
                    target=target,
                    communication_type='email',
                    recipient=recipient_email,
                    subject=subject,
                    message=message_body,
                    status='sent' if success else 'failed'
                )
                history_id = communication_history.id
            except Exception as db_error:
                # If the CommunicationHistory table doesn't exist, log and continue
                logging.warning(f"Could not save communication history: {str(db_error)}")
            
            if success:
                response_data = {'message': f'Email sent successfully to {recipient_email}'}
                if history_id:
                    response_data['history_id'] = history_id
                return Response(response_data)
            else:
                response_data = {'error': 'Failed to send email'}
                if history_id:
                    response_data['history_id'] = history_id
                return Response(response_data, status=500)
        
        except AlvoInvestigacao.DoesNotExist:
            return Response({'error': 'Target not found'}, status=404)
        except Exception as e:
            logging.exception(f"Error sending email for target {pk}: {str(e)}")
            return Response({'error': str(e)}, status=500)


class SendTestEmailView(APIView):
    permission_classes = []  # Removed authentication requirement
    
    def post(self, request):
        try:
            # Send test email
            success = send_test_email()
            
            if success:
                return Response({'message': 'Test email sent successfully'})
            else:
                return Response({'error': 'Failed to send test email'}, status=500)
        
        except Exception as e:
            logging.exception(f"Error sending test email: {str(e)}")
            return Response({'error': str(e)}, status=500)


class TargetCommunicationHistoryView(APIView):
    permission_classes = []  # Removed authentication requirement
    
    def get(self, request, pk):
        try:
            # Get the target instance
            target = AlvoInvestigacao.objects.get(pk=pk)
            
            # Get communication history for this target, with fallback if table doesn't exist
            try:
                communications = CommunicationHistory.objects.filter(target=target).order_by('-sent_at')
                
                # Serialize the data
                serializer = CommunicationHistoryListSerializer(communications, many=True)
                
                return Response({
                    'target_id': target.id,
                    'target_name': target.nome,
                    'communications': serializer.data
                })
            except Exception as db_error:
                # If the CommunicationHistory table doesn't exist, return empty history
                logging.warning(f"Could not retrieve communication history: {str(db_error)}")
                return Response({
                    'target_id': target.id,
                    'target_name': target.nome,
                    'communications': []
                })
        
        except AlvoInvestigacao.DoesNotExist:
            return Response({'error': 'Target not found'}, status=404)
        except Exception as e:
            logging.exception(f"Error retrieving communication history for target {pk}: {str(e)}")
            return Response({'error': str(e)}, status=500)


class FirestoreUsersView(APIView):
    """
    View to retrieve users from Firestore.
    Specifically designed to fetch users from the 'users' collection in Firestore.
    """
    permission_classes = []  # Removed authentication requirement
    
    def get(self, request):
        """
        Retrieve all users from Firestore 'users' collection.
        """
        try:
            users = get_firestore_collection('users')
            return Response({
                'success': True,
                'collection': 'users',
                'count': len(users),
                'data': users
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from .models import AlvoInvestigacao
from .serializers import AlvoInvestigacaoSerializer
from .sms_service import sms_service
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json

# New SMS sending view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_sms_to_suspect(request):
    """
    Send SMS to a suspect identified by their ID or phone number
    """
    try:
        data = request.data
        suspect_id = data.get('suspect_id')
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not message:
            return Response(
                {'error': 'Message content is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If suspect_id is provided, get the phone number from the suspect record
        if suspect_id:
            try:
                suspect = AlvoInvestigacao.objects.get(id=suspect_id)
                if not phone_number and hasattr(suspect, 'telefone'):
                    phone_number = suspect.telefone
            except AlvoInvestigacao.DoesNotExist:
                return Response(
                    {'error': 'Suspect not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Validate phone number
        if not phone_number:
            return Response(
                {'error': 'Phone number is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Handle both single phone number and list of phone numbers
        if isinstance(phone_number, list):
            # For TelcoSMS, we send one SMS at a time
            results = []
            for num in phone_number:
                success, result = send_sms_message(num, message)
                results.append({'phone_number': num, 'success': success, 'result': result})
            return Response({'results': results}, status=status.HTTP_200_OK)
        else:
            # Single phone number
            success, result = send_sms_message(phone_number, message)
            if success:
                return Response({'success': True, 'result': result}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Failed to send SMS', 'details': result}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from invasao.models import CapturedMedia, IntrusionSession
from invasao.serializers import CapturedMediaSerializer

from consulta_de_documentos.taxpayer_service import get_taxpayer_info
import requests

class TargetFullHistoryView(generics.RetrieveAPIView):
    """
    View to retrieve the full history of a target, including associated invasion media.
    """
    queryset = AlvoInvestigacao.objects.all()
    serializer_class = AlvoInvestigacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Fetch associated invasion media
        target_id_str = str(instance.id)
        
        # Try to extract suspect ID from observations
        # Format: "Adicionado a partir de suspeito ID: 494"
        suspect_id = None
        if instance.observacoes:
            import re
            match = re.search(r'suspeito ID:\s*(\d+)', instance.observacoes)
            if match:
                suspect_id = match.group(1)
                logging.info(f"Extracted suspect ID {suspect_id} from observations")
        
        # Search for sessions using both target ID and suspect ID
        sessions = IntrusionSession.objects.filter(
            models.Q(title__icontains=f"Suspect {target_id_str}") |
            (models.Q(title__icontains=f"Suspect {suspect_id}") if suspect_id else models.Q(pk=None))
        )
        
        logging.info(f"Found {sessions.count()} intrusion sessions for target {target_id_str} (suspect ID: {suspect_id})")
        
        media_files = CapturedMedia.objects.filter(session__in=sessions).order_by('-timestamp')
        logging.info(f"Found {media_files.count()} media files")
        
        media_serializer = CapturedMediaSerializer(media_files, many=True, context={'request': request})
        
        # Add media to the response data
        data['invasion_media'] = media_serializer.data

        # Fetch Deep Search Data (Identity)
        if instance.cpf:
            try:
                # Identity Service
                identity_url = f'https://consulta.edgarsingui.ao/consultar/{instance.cpf}'
                identity_response = requests.get(identity_url, timeout=10)
                if identity_response.status_code == 200:
                    data['deep_search_data'] = identity_response.json()
                
                # Taxpayer Service
                taxpayer_data = get_taxpayer_info(instance.cpf)
                if taxpayer_data:
                    data['taxpayer_data'] = taxpayer_data
            except Exception as e:
                print(f"Error fetching deep search data for target {instance.id}: {e}")
        
        return Response(data)
