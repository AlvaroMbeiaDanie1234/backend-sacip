import os
import requests
import base64
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

# Minio Configuration (Internal)
MINIO_HELPER_ENDPOINT = "http://10.110.71.14:9001/api/v1/download-shared-object"
MINIO_INTERNAL_BASE = "http://127.0.0.1:9000"
MINIO_BUCKET = "piips-test"

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_minio_file(request):
    """
    Proxy view to fetch files from Minio via helper service.
    Usage: /api/v1/sicgo/minio/file/?path=folder/sub/image.jpg
    """
    path = request.GET.get('path')
    if not path:
        return Response({'error': 'Path is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Construct internal URL to encode
    internal_url = f"{MINIO_INTERNAL_BASE}/{MINIO_BUCKET}/{path}"
    
    # Use urlsafe base64 and remove padding as some services are sensitive to it
    encoded_url = base64.urlsafe_b64encode(internal_url.encode()).decode().rstrip('=')
    
    helper_url = f"{MINIO_HELPER_ENDPOINT}/{encoded_url}"
    
    try:
        # Fetch from Helper Service
        response = requests.get(helper_url, stream=True, timeout=20)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            django_response = HttpResponse(response.content, content_type=content_type)
            # Add headers to prevent browser aborts and mixed content issues
            django_response["Access-Control-Allow-Origin"] = "*"
            django_response["Cache-Control"] = "public, max-age=3600"
            return django_response
        else:
            print(f"DEBUG: Minio Helper {response.status_code} for path: {path}")
            print(f"DEBUG: Helper URL attempted: {helper_url}")
            return HttpResponse(status=response.status_code)
            
    except Exception as e:
        print(f"DEBUG: Exception in Minio Proxy: {str(e)}")
        return HttpResponse(status=500)

PIIPS_URL = os.getenv('PIIPS_URL', 'http://10.110.71.5:3333/api/v1/sicgo')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_delituosos_procurados(request):
    """
    Proxy to fetch delituosos procurados from PIIPS API
    """
    try:
        url = f"{PIIPS_URL}/delituosos_procurados/public/todas"
        print(f"Calling PIIPS API: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        response = requests.get(url, headers=headers, timeout=30)
        print(f"PIIPS Response Status: {response.status_code}")
        data = response.json()
        print(f"PIIPS Data Sample: {str(data)[:200]}")
        return Response(data, status=response.status_code)
    except Exception as e:
        print(f"PIIPS API Error: {str(e)}")
        return Response({
            'error': 'Failed to connect to PIIPS API',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ocorrencias(request):
    """
    Proxy to fetch ocorrencias from PIIPS API
    """
    try:
        url = f"{PIIPS_URL}/ocorrencias/public/todas"
        print(f"Calling PIIPS API: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        response = requests.get(url, headers=headers, timeout=30)
        print(f"PIIPS Response Status: {response.status_code}")
        data = response.json()
        print(f"PIIPS Data Sample: {str(data)[:200]}")
        return Response(data, status=response.status_code)
    except Exception as e:
        print(f"PIIPS API Error: {str(e)}")
        return Response({
            'error': 'Failed to connect to PIIPS API',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_detido(request):
    """
    Proxy to fetch detidos from PIIPS API
    """
    try:
        url = f"{PIIPS_URL}/detido/public/todas"
        print(f"Calling PIIPS API: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        response = requests.get(url, headers=headers, timeout=30)
        print(f"PIIPS Response Status: {response.status_code}")
        data = response.json()
        print(f"PIIPS Data Sample: {str(data)[:200]}")
        return Response(data, status=response.status_code)
    except Exception as e:
        print(f"PIIPS API Error: {str(e)}")
        return Response({
            'error': 'Failed to connect to PIIPS API',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dinfop_delituoso(request):
    """
    Proxy to fetch dinfop delituosos from PIIPS API
    """
    try:
        url = f"{PIIPS_URL}/dinfop_delitouso/public/todas"
        print(f"Calling PIIPS API: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        response = requests.get(url, headers=headers, timeout=30)
        print(f"PIIPS Response Status: {response.status_code}")
        data = response.json()
        print(f"PIIPS Data Sample: {str(data)[:200]}")
        return Response(data, status=response.status_code)
    except Exception as e:
        print(f"PIIPS API Error: {str(e)}")
        return Response({
            'error': 'Failed to connect to PIIPS API',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
