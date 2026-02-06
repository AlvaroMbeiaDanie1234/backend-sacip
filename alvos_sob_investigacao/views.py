import logging
import uuid
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import AlvoInvestigacao
from .serializers import AlvoInvestigacaoSerializer
from .firebase_utils import get_firebase_data, get_firebase_record, search_firebase_data, get_multiple_firebase_paths
from .firestore_utils import get_firestore_collection, get_firestore_document, query_firestore_collection


class FirebaseDataView(APIView):
    """
    View to retrieve data from Firebase Realtime Database.
    Provides endpoints to fetch data from Firebase and return it to the frontend.
    """
    permission_classes = [permissions.IsAuthenticated]
    
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
    permission_classes = [permissions.IsAuthenticated]


class AlvoInvestigacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlvoInvestigacao.objects.all()
    serializer_class = AlvoInvestigacaoSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            # Get the target instance
            target = AlvoInvestigacao.objects.get(pk=pk)
            
            # Get recipient phone number and message from request
            recipient_phone = request.data.get('recipient_phone')
            message_body = request.data.get('message', '')
            
            # If no phone number provided in request, try to get it from the target record
            if not recipient_phone:
                recipient_phone = getattr(target, 'telefone', None)
            
            if not recipient_phone:
                return Response({'error': 'Recipient phone number is required'}, status=400)
            
            # Send SMS about the target
            success, result = send_sms_message(recipient_phone, message_body)
            
            if success:
                return Response({'message': f'SMS sent successfully to {recipient_phone}'})
            else:
                return Response({'error': 'Failed to send SMS', 'details': result}, status=500)
        
        except AlvoInvestigacao.DoesNotExist:
            return Response({'error': 'Target not found'}, status=404)
        except Exception as e:
            logging.exception(f"Error sending SMS for target {pk}: {str(e)}")
            return Response({'error': str(e)}, status=500)


class SendTestSmsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # Get the suspect ID from the request data
            suspect_id = request.data.get('suspect_id')
            
            if not suspect_id:
                return Response({'error': 'Suspect ID is required'}, status=400)
            
            # Get the suspect from informacoes_suspeitas app
            try:
                informacao_suspeita = InformacaoSuspeita.objects.get(id=suspect_id)
                suspect = informacao_suspeita.suspect
                
                # Check if suspect exists
                if not suspect:
                    return Response({'error': 'Suspect not associated with this information'}, status=400)
                    
            except InformacaoSuspeita.DoesNotExist:
                return Response({'error': 'Suspect information not found'}, status=404)
            except AttributeError:
                return Response({'error': 'Suspect not associated with this information'}, status=400)
            
            # Create a new investigation target based on the suspect
            # Only map fields that exist in the Suspect model
            full_name = getattr(suspect, 'full_name', 'Nome Desconhecido')
            suspect_nid = getattr(suspect, 'nid', '') or ''
            
            alvo_data = {
                'nome': full_name,
                'apelido': getattr(suspect, 'nickname', '') or '',
                'cpf': suspect_nid,  # Use NID field from suspect model
                'endereco': '',  # Suspect model doesn't have address field
                'telefone': '',  # Suspect model doesn't have phone field
                'email': '',  # Suspect model doesn't have email field
                'investigador_responsavel': request.user.id if request.user.is_authenticated else None,
                'observacoes': f'Adicionado a partir de informacao suspeita ID: {informacao_suspeita.id}',
                'status': 'ativo',  # Default status
            }
            
            # If no NID was provided, generate a default one to satisfy unique constraint
            if not suspect_nid:
                import uuid
                alvo_data['cpf'] = f"DEFAULT_{str(uuid.uuid4())[:8]}"
            
            # Map dangerous_level to nivel_prioridade if it exists
            if getattr(suspect, 'dangerous_level', None):
                # Map the dangerous level to priority level
                dangerous_level = getattr(suspect, 'dangerous_level', '').lower()
                if 'alta' in dangerous_level or 'high' in dangerous_level:
                    alvo_data['nivel_prioridade'] = 5
                elif 'media' in dangerous_level or 'medium' in dangerous_level:
                    alvo_data['nivel_prioridade'] = 3
                elif 'baixa' in dangerous_level or 'low' in dangerous_level:
                    alvo_data['nivel_prioridade'] = 1
            else:
                alvo_data['nivel_prioridade'] = 1  # Default priority level
            
            # Create the new target
            serializer = AlvoInvestigacaoSerializer(data=alvo_data)
            if serializer.is_valid():
                target = serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
                
        except Exception as e:
            logging.exception(f"Error adding suspect as target: {str(e)}")
            return Response({'error': str(e)}, status=500)


class SendTargetEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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
            
            if success:
                return Response({'message': f'Email sent successfully to {recipient_email}'})
            else:
                return Response({'error': 'Failed to send email'}, status=500)
        
        except AlvoInvestigacao.DoesNotExist:
            return Response({'error': 'Target not found'}, status=404)
        except Exception as e:
            logging.exception(f"Error sending email for target {pk}: {str(e)}")
            return Response({'error': str(e)}, status=500)


class SendTestEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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


class FirestoreUsersView(APIView):
    """
    View to retrieve users from Firestore.
    Specifically designed to fetch users from the 'users' collection in Firestore.
    """
    permission_classes = [permissions.IsAuthenticated]
    
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

