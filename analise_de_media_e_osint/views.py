import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

@api_view(['GET'])
def osint_search(request):
    """
    Perform OSINT search using SerpAPI
    """
    query = request.GET.get('q')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Get SerpAPI key from environment variable or settings
    serp_api_key = os.environ.get('SERPAPI_KEY') or getattr(settings, 'SERPAPI_KEY', None)
    if not serp_api_key or serp_api_key == 'your-serpapi-key-here':
        return Response({'error': 'SerpAPI key is not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        # Prepare parameters for SerpAPI
        params = {
            'engine': 'google',
            'q': query,
            'api_key': serp_api_key,
            'num': 10,
        }

        # Make request to SerpAPI
        serp_response = requests.get('https://serpapi.com/search', params=params)
        serp_response.raise_for_status()
        serp_data = serp_response.json()

        print('Resultado da pesquisa SerpAPI:', serp_data)

        images_results = (
            serp_data.get('images_results', []) or 
            serp_data.get('inline_images', []) or 
            []
        )

        formatted_response = {
            'success': True,
            'results': serp_data.get('organic_results', []),
            'images': images_results,  # Using the corrected images data
            'total': serp_data.get('search_information', {}).get('total_results', 0),
            'query': serp_data.get('search_information', {}).get('query_displayed', query),
        }

        # Print formatted response to console for debugging
        print('Resposta formatada para o frontend:', formatted_response)

        return Response(formatted_response)
    except requests.exceptions.RequestException as e:
        print('OSINT search error:', str(e))
        return Response({'error': 'Failed to perform OSINT search'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print('Unexpected error:', str(e))
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)