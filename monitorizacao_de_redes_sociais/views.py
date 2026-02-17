from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import PerfilRedeSocial, Postagem, AlertaMonitoramento, LinkRedeSocialAlvo
from .serializers import PerfilRedeSocialSerializer, PostagemSerializer, AlertaMonitoramentoSerializer, LinkRedeSocialAlvoSerializer
from .scraper import SocialMediaScraperService
from alvos_sob_investigacao.firestore_utils import get_firestore_collection
from django.db.models import Prefetch
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
from threading import Thread
import subprocess
import os
import json


class PerfilRedeSocialListCreateView(generics.ListCreateAPIView):
    queryset = PerfilRedeSocial.objects.all()
    serializer_class = PerfilRedeSocialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(monitorado_por=self.request.user)


class PerfilRedeSocialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerfilRedeSocial.objects.all()
    serializer_class = PerfilRedeSocialSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostagemListCreateView(generics.ListCreateAPIView):
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostagemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlertaMonitoramentoListCreateView(generics.ListCreateAPIView):
    queryset = AlertaMonitoramento.objects.all()
    serializer_class = AlertaMonitoramentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(monitorado_por=self.request.user)


class AlertaMonitoramentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlertaMonitoramento.objects.all()
    serializer_class = AlertaMonitoramentoSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def sync_profile_data(request, perfil_id):
    """Sync profile data from social media platform"""
    scraper_service = SocialMediaScraperService()
    success = scraper_service.sync_profile_data(perfil_id)
    
    if success:
        return Response({'message': 'Profile data synced successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Failed to sync profile data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sync_profile_posts(request, perfil_id):
    """Sync posts from a social media profile"""
    limit = request.data.get('limit', 10)
    scraper_service = SocialMediaScraperService()
    new_posts_count = scraper_service.sync_profile_posts(perfil_id, limit)
    
    return Response({
        'message': f'Synced {new_posts_count} new posts',
        'new_posts_count': new_posts_count
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def scrape_profile_and_posts(request, perfil_id):
    """Complete sync of profile and posts"""
    limit = request.data.get('limit', 10)
    scraper_service = SocialMediaScraperService()
    result = scraper_service.scrape_profile_and_posts(perfil_id, limit)
    
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def scrape_platform_posts(request, plataforma):
    """Scrape multiple profiles from a specific platform"""
    limit = request.GET.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    
    scraper_service = SocialMediaScraperService()
    results = scraper_service.scrape_by_platform(plataforma, limit)
    
    return Response(results, status=status.HTTP_200_OK)


@api_view(['POST'])
def scrape_generic_content(request):
    """Scrape generic social media content from a URL"""
    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    scraper_service = SocialMediaScraperService()
    posts = scraper_service.scraper.scrape_generic_social_content(url)
    
    return Response({'posts': posts, 'count': len(posts)}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_atividades_monitorizadas(request):
    """Get all posts with related profile information for monitoring display"""
    try:
        # Get posts with related profile data
        posts = Postagem.objects.select_related('perfil').all()
        
        # Format the data to match the frontend's expectations
        atividades = []
        for post in posts:
            atividade = {
                'id': post.id,
                'perfil': post.perfil.id,
                'post_id': post.post_id,
                'conteudo': post.conteudo,
                'data_postagem': post.data_postagem.isoformat() if post.data_postagem else None,
                'curtidas': post.curtidas,
                'compartilhamentos': post.compartilhamentos,
                'comentarios': post.comentarios,
                'url_postagem': post.url_postagem,
                'marcadores': post.marcadores,
                'relevancia': post.relevancia,
                'data_coleta': post.data_coleta.isoformat() if post.data_coleta else None,
                'plataforma': post.perfil.plataforma,
                'nome_usuario': post.perfil.nome_usuario,
            }
            atividades.append(atividade)
        
        return Response(atividades, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_google_alerts_rss(request):
    """Get Google Alerts RSS feed data similar to the example implementation"""
    try:
        # In a real implementation, this would fetch from configured Google Alert RSS feeds
        # For now, we'll simulate the functionality based on the main.py example
        
        # This would typically come from a model that stores Google Alert configurations
        # For demo purposes, I'll create a function that mimics the main.py functionality
        def get_clean_url(google_proxy_url: str) -> str:
            """Remove Google redirect and get the actual URL"""
            match = re.search(r'[?&]url=([^&]+)', google_proxy_url)
            if match:
                import urllib.parse
                return urllib.parse.unquote(match.group(1))
            
            # Fallback: try to follow redirect (may fail in some cases)
            try:
                response = requests.get(google_proxy_url, timeout=8, allow_redirects=True)
                return response.url
            except Exception:
                return google_proxy_url
        
        # Sample Google Alert RSS feed URL (would be configurable in real implementation)
        # For demonstration, I'll create mock data similar to main.py
        sample_alerts = []
        
        # In a real implementation, we would fetch from actual Google Alerts RSS feed like:
        # response = requests.get(RSS_FEED_URL, headers=headers, timeout=12)
        # soup = BeautifulSoup(response.text, "xml")
        # entries = soup.find_all("entry")
        # 
        # For now, return sample data that follows the same structure as main.py
        sample_alerts = [
            {
                "title": "Pessoa de Interesse mencionada em notícia",
                "published": "2025-12-24T10:30:00Z",
                "url": "https://noticiaexemplo.com/pessoa-interesse",
                "content": "Conteúdo do alerta do Google com menções relevantes a pessoas ou termos de interesse...",
                "source": "Exemplo de Fonte de Notícia"
            },
            {
                "title": "Menção em redes sociais sobre tópico monitorado",
                "published": "2025-12-24T09:15:00Z", 
                "url": "https://redeexemplo.com/mencao",
                "content": "Outra menção relevante detectada por meio do sistema de alertas...",
                "source": "Exemplo de Rede Social"
            }
        ]
        
        return Response(sample_alerts, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_google_alert(request):
    """Add a new Google Alert RSS feed to monitor"""
    try:
        # Extract data from request
        feed_url = request.data.get('feed_url')
        name = request.data.get('name', 'Google Alert')
        
        if not feed_url:
            return Response({'error': 'Feed URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # In a real implementation, we would validate the RSS feed and store it
        # For now, return success
        return Response({
            'message': 'Google Alert added successfully',
            'name': name,
            'feed_url': feed_url
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def criar_alerta_monitoramento(request):
    """Create a new monitoring alert for a search term"""
    if not request.user.is_authenticated:
        return Response({'error': 'Usuário não autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        
    try:
        termo_busca = request.data.get('termo_busca')
        descricao = request.data.get('descricao', '')
        
        if not termo_busca:
            return Response({'error': 'Termo de busca é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the alert
        alerta = AlertaMonitoramento.objects.create(
            termo_busca=termo_busca,
            descricao=descricao,
            ativo=True,
            monitorado_por=request.user
        )
        
        serializer = AlertaMonitoramentoSerializer(alerta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def buscar_resultados_alerta(request, alerta_id):
    """Search for results related to a specific alert"""
    try:
        alerta = AlertaMonitoramento.objects.get(id=alerta_id)
        
        # In a real implementation, this would search the internet for the term
        # For now, we'll return mock results
        # In practice, this would use search engines APIs or web scraping
        
        # Update the last checked time
        alerta.data_ultima_verificacao = datetime.now()
        alerta.save()
        
        # Mock search results
        resultados = [
            {
                "titulo": f"Resultado para '{alerta.termo_busca}' - Notícia Exemplo",
                "descricao": f"Esta é uma notícia que menciona o termo '{alerta.termo_busca}' em um contexto relevante.",
                "url": "https://exemplo.com/noticia",
                "fonte": "Exemplo de Fonte",
                "data": datetime.now().isoformat()
            }
        ]
        
        return Response(resultados, status=status.HTTP_200_OK)
    except AlertaMonitoramento.DoesNotExist:
        return Response({'error': 'Alerta não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def buscar_todos_alertas_resultados(request):
    """Search for results for all active alerts"""
    try:
        alertas = AlertaMonitoramento.objects.filter(ativo=True)
        resultados_completos = []
        
        for alerta in alertas:
            # In a real implementation, this would search the internet for the term
            # For now, we'll return mock results
            resultados = [
                {
                    "alerta_id": alerta.id,
                    "termo_busca": alerta.termo_busca,
                    "resultados": [
                        {
                            "titulo": f"Resultado para '{alerta.termo_busca}'",
                            "descricao": f"Menção encontrada para o termo '{alerta.termo_busca}'",
                            "url": "https://exemplo.com/mencao",
                            "fonte": "Fonte Exemplo",
                            "data": datetime.now().isoformat()
                        }
                    ]
                }
            ]
            resultados_completos.extend(resultados)
        
        # Update the last checked time for all alerts
        alertas.update(data_ultima_verificacao=datetime.now())
        
        return Response(resultados_completos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_nossa_comunidade_users(request):
    """
    Get users from Firestore 'users' collection for the 'Nossa Comunidade' section.
    """
    try:
        users = get_firestore_collection('users')
        
        # Format the users to match the frontend requirements
        formatted_users = []
        for user in users:
            formatted_user = {
                'id': user.get('id'),
                'nome': user.get('nome', ''),
                'email': user.get('email', ''),
                'fotoPerfil': user.get('fotoPerfil', ''),
                'bio': user.get('bio', ''),
                'morada': user.get('morada', ''),
                'dataNascimento': user.get('dataNascimento', ''),
                'lastActive': user.get('lastActive', ''),
                'fcmToken': user.get('fcmToken', ''),
                'telefone': user.get('telefone', ''),
                'photos': user.get('photos', []),
                'statuses': user.get('statuses', [])
            }
            formatted_users.append(formatted_user)
        
        return Response({
            'success': True,
            'collection': 'users',
            'count': len(formatted_users),
            'data': formatted_users
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- Links redes sociais associados a alvos (Sherlock) ---
try:
    from alvos_sob_investigacao.models import AlvoInvestigacao
except ImportError:
    AlvoInvestigacao = None


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def associar_perfil_alvo(request):
    """Associa um link de rede social (ex: resultado Sherlock) a um alvo."""
    alvo_id = request.data.get('alvo_id')
    nome_site = request.data.get('nome_site')
    url_perfil = request.data.get('url_perfil')
    if not alvo_id or not nome_site or not url_perfil:
        return Response(
            {'error': 'alvo_id, nome_site e url_perfil são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        link, created = LinkRedeSocialAlvo.objects.get_or_create(
            alvo_id=int(alvo_id),
            nome_site=nome_site.strip(),
            defaults={
                'url_perfil': url_perfil.strip(),
                'associado_por': request.user if request.user.is_authenticated else None,
            }
        )
        if not created:
            link.url_perfil = url_perfil.strip()
            link.associado_por = request.user if request.user.is_authenticated else None
            link.save(update_fields=['url_perfil', 'associado_por'])
        return Response(LinkRedeSocialAlvoSerializer(link).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def listar_links_alvo(request):
    """Lista links associados a um alvo (query: ?alvo_id=)."""
    alvo_id = request.query_params.get('alvo_id')
    if not alvo_id:
        return Response({'error': 'alvo_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    links = LinkRedeSocialAlvo.objects.filter(alvo_id=int(alvo_id)).order_by('-data_associacao')
    return Response(LinkRedeSocialAlvoSerializer(links, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def alvos_com_links(request):
    """Lista alvos que têm pelo menos um link de rede social associado, com os links (para cards em Atividades Recentes)."""
    from collections import defaultdict
    links = LinkRedeSocialAlvo.objects.all().order_by('alvo_id', '-data_associacao')
    by_alvo = defaultdict(list)
    for link in links:
        by_alvo[link.alvo_id].append(LinkRedeSocialAlvoSerializer(link).data)
    alvo_ids = list(by_alvo.keys())
    if not alvo_ids:
        return Response([], status=status.HTTP_200_OK)
    nomes = {}
    if AlvoInvestigacao:
        for a in AlvoInvestigacao.objects.filter(id__in=alvo_ids).values('id', 'nome', 'email'):
            nomes[a['id']] = {'nome': a['nome'], 'email': a.get('email', '')}
    result = [
        {
            'alvo_id': aid,
            'alvo_nome': nomes.get(aid, {}).get('nome', f'Alvo #{aid}'),
            'alvo_email': nomes.get(aid, {}).get('email', ''),
            'links': by_alvo[aid],
        }
        for aid in sorted(alvo_ids)
    ]
    return Response(result, status=status.HTTP_200_OK)


from .sherlock_project.sherlock import sherlock
from .sherlock_project.sites import SitesInformation
from .sherlock_project.notify import QueryNotify
from .sherlock_project.result import QueryStatus
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import queue

class ResultCollector(QueryNotify):
    def __init__(self):
        super().__init__()
        self.found_results = []

    def update(self, result):
        if result.status == QueryStatus.CLAIMED:
            self.found_results.append({
                'site': result.site_name,
                'url': result.site_url_user,
            })


class StreamingResultCollector(QueryNotify):
    """Collector that pushes each result to a queue for SSE streaming."""
    SENTINEL = None  # end of stream

    def __init__(self, result_queue):
        super().__init__()
        self.result_queue = result_queue

    def start(self, message=None):
        self.result_queue.put({'type': 'start', 'username': message or ''})

    def update(self, result):
        if result.status == QueryStatus.CLAIMED:
            self.result_queue.put({
                'type': 'result',
                'site': result.site_name,
                'url': result.site_url_user,
            })

    def finish(self, message=None):
        self.result_queue.put({'type': 'done'})
        self.result_queue.put(StreamingResultCollector.SENTINEL)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sherlock_search(request):
    """
    Execute internal sherlock search for a given username.
    """
    username = request.data.get('username')
    nsfw = request.data.get('nsfw', False)
    timeout = request.data.get('timeout', 60)
    
    if not username:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Load sites from the internal resources
        data_file_path = os.path.join(os.path.dirname(__file__), 'sherlock_project', 'resources', 'data.json')
        
        if not os.path.exists(data_file_path):
            return Response({'error': f'Sherlock data file not found at {data_file_path}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        sites = SitesInformation(data_file_path=data_file_path)
        
        if not nsfw:
            sites.remove_nsfw_sites()
            
        site_data = {site.name: site.information for site in sites}
        
        # Initialize our result collector
        collector = ResultCollector()
        
        # Execute sherlock search programmatically
        # This will run in the main thread (synchronously within the view)
        # The timeout here is per-site request
        results_raw = sherlock(
            username=username,
            site_data=site_data,
            query_notify=collector,
            timeout=timeout,
            dump_response=False
        )
        
        return Response({
            'username': username,
            'results': collector.found_results,
            'count': len(collector.found_results),
            'status': 'completed'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _sherlock_stream_generator(username, result_queue, data_file_path, nsfw=False, timeout=60):
    """Generator that yields SSE events from the queue while sherlock runs in a thread."""
    def run_sherlock():
        try:
            sites = SitesInformation(data_file_path=data_file_path)
            if not nsfw:
                sites.remove_nsfw_sites()
            site_data = {site.name: site.information for site in sites}
            collector = StreamingResultCollector(result_queue)
            sherlock(
                username=username,
                site_data=site_data,
                query_notify=collector,
                timeout=timeout,
                dump_response=False,
            )
        except Exception as e:
            import traceback
            result_queue.put({'type': 'error', 'error': str(e), 'traceback': traceback.format_exc()})
        result_queue.put(StreamingResultCollector.SENTINEL)

    t = Thread(target=run_sherlock)
    t.start()

    while True:
        item = result_queue.get()
        if item is StreamingResultCollector.SENTINEL:
            break
        yield f"data: {json.dumps(item)}\n\n"

    t.join(timeout=1)


@require_http_methods(["POST"])
@csrf_exempt
def sherlock_search_stream(request):
    """
    Execute Sherlock search and stream each result as Server-Sent Events (SSE).
    Plain Django view to avoid DRF content negotiation (406) for text/event-stream.
    """
    try:
        body = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return HttpResponse(
            json.dumps({'error': 'Invalid JSON body'}),
            status=400,
            content_type='application/json',
        )
    username = body.get('username')
    nsfw = body.get('nsfw', False)
    timeout = body.get('timeout', 60)

    if not username:
        return HttpResponse(
            json.dumps({'error': 'Username is required'}),
            status=400,
            content_type='application/json',
        )

    data_file_path = os.path.join(os.path.dirname(__file__), 'sherlock_project', 'resources', 'data.json')
    if not os.path.exists(data_file_path):
        return HttpResponse(
            json.dumps({'error': f'Sherlock data file not found at {data_file_path}'}),
            status=500,
            content_type='application/json',
        )

    result_queue = queue.Queue()
    response = StreamingHttpResponse(
        _sherlock_stream_generator(username, result_queue, data_file_path, nsfw=nsfw, timeout=timeout),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


# --- Holehe (Email Search) ---

def _holehe_stream_generator(email, result_queue):
    """Generator that yields SSE events from the queue while holehe runs in a thread."""
    def run_holehe():
        try:
            import trio
            import httpx
            from holehe.core import import_submodules, get_functions, launch_module

            # Import modules from the installed holehe package
            modules = import_submodules("holehe.modules")

            class MockArgs:
                nopasswordrecovery = False

            websites = get_functions(modules, MockArgs())

            result_queue.put({'type': 'start', 'email': email, 'total': len(websites)})

            async def main_holehe_async():
                client = httpx.AsyncClient(timeout=10)
                out = []

                async with trio.open_nursery() as nursery:
                    for website in websites:
                        nursery.start_soon(launch_module, website, email, client, out)

                await client.aclose()

                # Process all results after completion
                for res in out:
                    if res.get("exists"):
                        result_queue.put({
                            'type': 'result',
                            'site': res.get("name", res.get("domain", "unknown")),
                            'url': res.get("domain", ""),
                            'emailrecovery': res.get("emailrecovery"),
                            'phoneNumber': res.get("phoneNumber"),
                        })

                result_queue.put({'type': 'done', 'total_checked': len(out)})
                result_queue.put(StreamingResultCollector.SENTINEL)

            trio.run(main_holehe_async)
        except Exception as e:
            import traceback
            result_queue.put({'type': 'error', 'error': str(e), 'traceback': traceback.format_exc()})
            result_queue.put(StreamingResultCollector.SENTINEL)

    t = Thread(target=run_holehe)
    t.start()

    while True:
        item = result_queue.get()
        if item is StreamingResultCollector.SENTINEL:
            break
        yield f"data: {json.dumps(item)}\n\n"

    t.join(timeout=1)


@require_http_methods(["POST"])
@csrf_exempt
def holehe_search_stream(request):
    """
    Execute Holehe search for a given email and stream results.
    """
    try:
        body = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return HttpResponse(
            json.dumps({'error': 'Invalid JSON body'}),
            status=400,
            content_type='application/json',
        )

    email = body.get('email')
    if not email:
        return HttpResponse(
            json.dumps({'error': 'Email is required'}),
            status=400,
            content_type='application/json',
        )

    result_queue = queue.Queue()
    response = StreamingHttpResponse(
        _holehe_stream_generator(email, result_queue),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response

