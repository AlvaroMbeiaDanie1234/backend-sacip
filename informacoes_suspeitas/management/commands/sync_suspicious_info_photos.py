from django.core.management.base import BaseCommand
from django.conf import settings
from informacoes_suspeitas.models import InformacaoSuspeita
from facial_recognition.models import Suspect
from users.models import User
import requests
from pathlib import Path
import urllib.parse


class Command(BaseCommand):
    help = 'Sync suspicious information photos from external API to local media folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of records to process',
            default=None
        )

    def handle(self, *args, **options):
        self.stdout.write('Fetching suspicious information from external API...')
        
        EXTERNAL_API_URL = 'http://10.110.2.220:3333/api/v1/inteligency/actions-suspectius'
        MEDIA_ROOT = Path(settings.MEDIA_ROOT) / 'suspicious_info_photos'
        MEDIA_ROOT.mkdir(exist_ok=True, parents=True)

        try:
            response = requests.get(EXTERNAL_API_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            suspicious_data = data.get('object', [])
            limit = options.get('limit')
            if limit:
                suspicious_data = suspicious_data[:limit]
                
            self.stdout.write(f'Found {len(suspicious_data)} suspicious information records in the external API.')
            
            default_user = User.objects.first()
            if not default_user:
                self.stdout.write("No users found, creating a default user...")
                default_user = User.objects.create_user(
                    username='system',
                    email='system@sacip.ao',
                    password='default_password'
                )
            
            for i, info_data in enumerate(suspicious_data):
                try:
                    title = info_data.get('description', f"Suspicious Info {info_data.get('id', i)}") or f"Suspicious Info {info_data.get('id', i+1)}"
                    description = info_data.get('description', '') or ''
                    source = info_data.get('origin_information', 'External API') or 'External API'
                    photo_url = info_data.get('photo', '') or ''
                    full_name = info_data.get('full_name', '') or ''
                    service = info_data.get('service', '') or ''
                    
                    suspect = None
                    if full_name:
                        suspects_with_name = Suspect.objects.filter(full_name=full_name)
                        if suspects_with_name.exists():
                            suspect = suspects_with_name.first()
                        else:
                            suspect = Suspect.objects.create(
                                full_name=full_name,
                                nickname=info_data.get('nickname', ''),
                                dangerous_level=info_data.get('dangerous', ''),
                                dangerous_color=info_data.get('dangerous_color', '')
                            )
                    
                    photo_path = None
                    if photo_url:
                        existing_info = InformacaoSuspeita.objects.filter(id=info_data.get('id')).first()
                        if existing_info and existing_info.photo:
                            self.stdout.write(f'Skipping download for {title} - photo already exists')
                            photo_path = existing_info.photo
                        else:
                            filename = f"info_{info_data.get('id', i+1)}_{full_name.replace(' ', '_')}" if info_data.get('id') else f"info_{i+1}_{full_name.replace(' ', '_')}"
                            filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
                            photo_path = self.download_image_from_url(photo_url, filename, MEDIA_ROOT)
                    
                    informacao_suspeita, created = InformacaoSuspeita.objects.get_or_create(
                        id=info_data.get('id', i+1),
                        defaults={
                            'titulo': title,
                            'descricao': description,
                            'fonte': source,
                            'nivel_confianca': info_data.get('level', 1),
                            'criado_por': default_user,
                            'suspect': suspect,
                        }
                    )
                    
                    informacao_suspeita.titulo = title
                    informacao_suspeita.descricao = description
                    informacao_suspeita.fonte = source
                    informacao_suspeita.nivel_confianca = info_data.get('level', 1)
                    informacao_suspeita.suspect = suspect
                    
                    if photo_path:
                        informacao_suspeita.photo = photo_path
                    
                    informacao_suspeita.save()
                    
                    if created:
                        self.stdout.write(f"Added new suspicious information: {title}")
                    else:
                        self.stdout.write(f"Updated existing suspicious information: {title}")
                        
                except Exception as e:
                    self.stdout.write(f"Error processing suspicious info {info_data.get('id', i+1)}: {e}")
                    continue
            
            self.stdout.write(
                self.style.SUCCESS('Finished syncing suspicious information.')
            )
            
        except Exception as e:
            self.stdout.write(f"Error fetching suspicious information data: {e}")

    def download_image_from_url(self, image_url, filename, MEDIA_ROOT):
        try:
            if image_url.startswith('/'):
                encoded_path = urllib.parse.quote(image_url, safe='')
                image_url = f'http://10.110.2.220:3333/api/v1/files?url={encoded_path}'
            elif 'api.sgcei.cacc.ao/api/v1/files?url=' in image_url:
                pass
            
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                extension = '.jpg'
            elif 'png' in content_type:
                extension = '.png'
            elif 'gif' in content_type:
                extension = '.gif'
            else:
                from urllib.parse import urlparse
                parsed_url = urlparse(image_url)
                path = parsed_url.path
                if '.' in path:
                    extension = '.' + path.split('.')[-1]
                else:
                    extension = '.jpg'
            
            filepath = MEDIA_ROOT / f"{filename}{extension}"
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return str(filepath.relative_to(settings.MEDIA_ROOT))
        except Exception as e:
            self.stdout.write(f"Error downloading image from {image_url}: {e}")
            return None
