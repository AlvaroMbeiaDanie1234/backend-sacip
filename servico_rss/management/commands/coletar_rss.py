from django.core.management.base import BaseCommand
from servico_rss.views import ColetarNoticiasRSSView
from django.http import HttpRequest
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Coleta notícias dos feeds RSS configurados'

    def add_arguments(self, parser):
        parser.add_argument('--user-id', type=int, help='ID do usuário para autenticação')

    def handle(self, *args, **options):
        # Create a mock request
        request = HttpRequest()
        
        # If user-id is provided, authenticate the request
        if options['user_id']:
            try:
                user = User.objects.get(id=options['user_id'])
                request.user = user
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Usuário com ID {options["user_id"]} não encontrado')
                )
                return
        
        # Create an instance of the view and call the post method
        view = ColetarNoticiasRSSView()
        view.request = request
        
        try:
            response = view.post(request)
            self.stdout.write(
                self.style.SUCCESS(response.data['message'])
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao coletar notícias: {str(e)}')
            )