import feedparser
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime
import email.utils
from .models import FonteRSS, NoticiaRSS
from .serializers import FonteRSSSerializer, NoticiaRSSSerializer
from django.db.models import Q

class FonteRSSListCreateView(generics.ListCreateAPIView):
    queryset = FonteRSS.objects.all()
    serializer_class = FonteRSSSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(adicionado_por=self.request.user)

class FonteRSSDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FonteRSS.objects.all()
    serializer_class = FonteRSSSerializer
    permission_classes = [permissions.IsAuthenticated]

class NoticiaRSSListView(generics.ListAPIView):
    queryset = NoticiaRSS.objects.all()
    serializer_class = NoticiaRSSSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = NoticiaRSS.objects.all()
        fonte_id = self.request.query_params.get('fonte_id', None)
        search_query = self.request.query_params.get('search', None)
        
        if fonte_id is not None:
            queryset = queryset.filter(fonte_id=fonte_id)
            
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(descricao__icontains=search_query) |
                Q(conteudo__icontains=search_query) |
                Q(autor__icontains=search_query)
            )
            
        return queryset

class ColetarNoticiasRSSView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def parse_date(self, date_str):
        """
        Parse RSS date string to datetime object
        """
        if not date_str:
            return timezone.now()
        
        try:
            # Try to parse with email.utils (RFC 2822 format)
            parsed = email.utils.parsedate_to_datetime(date_str)
            if parsed:
                return parsed
        except (TypeError, ValueError):
            pass
        
        try:
            # Try ISO format
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            pass
        
        # If all parsing attempts fail, return current time
        return timezone.now()
    
    def post(self, request):
        """
        Manually trigger RSS feed collection
        """
        fontes = FonteRSS.objects.filter(ativa=True)
        noticias_coletadas = 0
        
        for fonte in fontes:
            try:
                feed = feedparser.parse(fonte.url)
                for entry in feed.entries:
                    # Create or update news article
                    noticia, created = NoticiaRSS.objects.update_or_create(
                        url=entry.link,
                        defaults={
                            'titulo': entry.title,
                            'descricao': getattr(entry, 'summary', ''),
                            'data_publicacao': self.parse_date(getattr(entry, 'published', None)),
                            'autor': getattr(entry, 'author', ''),
                            'conteudo': getattr(entry, 'content', [{'value': ''}])[0].get('value', '') if hasattr(entry, 'content') else '',
                            'fonte': fonte,
                        }
                    )
                    if created:
                        noticias_coletadas += 1
            except Exception as e:
                print(f"Error processing feed {fonte.url}: {str(e)}")
                continue
                
        return Response({
            'message': f'Coleta de notícias concluída. {noticias_coletadas} novas notícias coletadas.',
            'novas_noticias': noticias_coletadas
        }, status=status.HTTP_200_OK)