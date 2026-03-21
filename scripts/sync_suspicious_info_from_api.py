#!/usr/bin/env python
"""
Script to sync suspicious information from the external API to the local database
and save photos to the local media folder.
"""
import os
import sys
import django
import requests
from pathlib import Path
from urllib.parse import urlparse, urljoin

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

# Import Django models after setting up Django
from informacoes_suspeitas.models import InformacaoSuspeita
from facial_recognition.models import Suspect
from users.models import User
from django.core.files.base import ContentFile
from urllib.parse import unquote

# Configuration
EXTERNAL_API_URL = 'http://10.110.2.220:3333/api/v1/inteligency/actions-suspectius'
MEDIA_ROOT = Path('media')
MEDIA_ROOT.mkdir(exist_ok=True, parents=True)

def download_image_from_url(image_url, filename):
    """Download an image from a URL and save it to the media folder."""
    try:
        # Handle relative URLs by making them go through the proxy endpoint
        if image_url.startswith('/'):
            # URL encode the relative path
            import urllib.parse
            encoded_path = urllib.parse.quote(image_url, safe='')
            image_url = f'http://10.110.2.220:3333/api/v1/files?url={encoded_path}'
        # Handle the API URL format where the actual image URL is encoded
        elif 'api.sgcei.cacc.ao/api/v1/files?url=' in image_url:
            # The URL is already in the correct format, use as is
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
            parsed_url = urlparse(image_url)
            path = parsed_url.path
            if '.' in path:
                extension = '.' + path.split('.')[-1]
            else:
                extension = '.jpg'  # default
        
        # Create a unique filename
        filepath = MEDIA_ROOT / f"{filename}{extension}"
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return str(filepath.relative_to('media'))
    except Exception as e:
        print(f"Error downloading image from {image_url}: {e}")
        return None


def sync_suspicious_info():
    """Sync suspicious information from external API to local database."""
    print("Fetching suspicious information from external API...")
    
    try:
        # Fetch data from external API
        response = requests.get(EXTERNAL_API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        suspicious_data = data.get('object', [])
        print(f"Found {len(suspicious_data)} suspicious information records in the external API.")
        
        # Get a default user for creating records (using the first user in the system)
        default_user = User.objects.first()
        if not default_user:
            print("No users found, creating a default user...")
            default_user = User.objects.create_user(
                username='system',
                email='system@sacip.ao',
                password='default_password'
            )
        
        # Process each suspicious information record
        for i, info_data in enumerate(suspicious_data):
            try:
                # Extract information
                title = info_data.get('description', f"Suspicious Info {info_data.get('id', i)}") or f"Suspicious Info {info_data.get('id', i+1)}"
                description = info_data.get('description', '') or ''
                source = info_data.get('origin_information', 'External API') or 'External API'
                photo_url = info_data.get('photo', '') or ''
                full_name = info_data.get('full_name', '') or ''
                service = info_data.get('service', '') or ''
                
                # Find or create associated suspect if exists
                suspect = None
                if full_name:
                    # Try to find existing suspect by full name, using filter to avoid multiple results
                    suspects_with_name = Suspect.objects.filter(full_name=full_name)
                    if suspects_with_name.exists():
                        # Get the first suspect if multiple exist
                        suspect = suspects_with_name.first()
                    else:
                        # Create a new suspect if not found
                        suspect = Suspect.objects.create(
                            full_name=full_name,
                            nickname=info_data.get('nickname', ''),
                            dangerous_level=info_data.get('dangerous', ''),
                            dangerous_color=info_data.get('dangerous_color', '')
                        )
                
                # Download photo if available
                photo_path = None
                if photo_url:
                    # Create a filename based on the info ID or full name
                    filename = f"info_{info_data.get('id', i+1)}_{full_name.replace(' ', '_')}" if info_data.get('id') else f"info_{i+1}_{full_name.replace(' ', '_')}"
                    filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
                    photo_path = download_image_from_url(photo_url, filename)
                
                # Create or update the suspicious information record
                informacao_suspeita, created = InformacaoSuspeita.objects.get_or_create(
                    id=info_data.get('id', i+1),  # Use external ID if available
                    defaults={
                        'titulo': title,
                        'descricao': description,
                        'fonte': source,
                        'nivel_confianca': info_data.get('level', 1),
                        'criado_por': default_user,
                        'suspect': suspect,
                    }
                )
                
                # Update fields that might have changed
                informacao_suspeita.titulo = title
                informacao_suspeita.descricao = description
                informacao_suspeita.fonte = source
                informacao_suspeita.nivel_confianca = info_data.get('level', 1)
                informacao_suspeita.suspect = suspect
                
                # Set the photo if we successfully downloaded it
                if photo_path:
                    # We need to save the relative path to the photo field
                    informacao_suspeita.photo = photo_path
                
                informacao_suspeita.save()
                
                if created:
                    print(f"Added new suspicious information: {title}")
                else:
                    print(f"Updated existing suspicious information: {title}")
                    
            except Exception as e:
                print(f"Error processing suspicious info {info_data.get('id', i+1)}: {e}")
                continue
        
        print("Finished syncing suspicious information.")
        
    except Exception as e:
        print(f"Error fetching suspicious information data: {e}")


if __name__ == "__main__":
    sync_suspicious_info()