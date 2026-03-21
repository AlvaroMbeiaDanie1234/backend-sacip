#!/usr/bin/env python
"""
Script to populate the suspects database with data from the external API
and generate face embeddings using InsightFace.
"""

import os
import sys
import django
import requests
import cv2
import numpy as np
from pathlib import Path

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

# Import Django models after setting up Django
from facial_recognition.models import Suspect

# Import InsightFace
try:
    from insightface.app import FaceAnalysis
    INSIGHTFACE_AVAILABLE = True
except ImportError:
    INSIGHTFACE_AVAILABLE = False
    print("InsightFace not available. Facial recognition will be disabled.")

# Configuration
MODEL_NAME = 'buffalo_l'
EXTERNAL_API_URL = 'http://10.110.2.220:3333/api/v1/inteligency/actions-suspectius'
MEDIA_ROOT = Path(__file__).parent.parent / 'media'

# Create media directory if it doesn't exist
MEDIA_ROOT.mkdir(exist_ok=True)

# Initialize FaceAnalysis
if INSIGHTFACE_AVAILABLE:
    face_app = FaceAnalysis(name=MODEL_NAME, providers=['CPUExecutionProvider'], root=Path("models"))
    face_app.prepare(ctx_id=0, det_size=(640, 640))
else:
    face_app = None


def download_image(url, save_path):
    """Download an image from a URL and save it locally."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return False


def extract_face_embedding(image_path):
    """Extract face embedding from an image using InsightFace."""
    if not INSIGHTFACE_AVAILABLE:
        return None
        
    try:
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Could not read image: {image_path}")
            return None
            
        # Detect faces
        faces = face_app.get(img)
        if not faces:
            print(f"No faces detected in image: {image_path}")
            return None
            
        # Return the first face embedding
        return faces[0].embedding.tolist()
    except Exception as e:
        print(f"Error extracting face embedding from {image_path}: {e}")
        return None


def create_placeholder_image(filepath, text):
    """Create a placeholder image with text."""
    # Create a black image
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Add text to the image
    # Center the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2
    
    cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
    
    # Save the image
    cv2.imwrite(str(filepath), img)


def populate_suspects():
    """Populate the suspects database with data from the external API."""
    if not INSIGHTFACE_AVAILABLE:
        print("InsightFace is not available. Cannot extract face embeddings.")
        return
        
    print("Fetching suspects data from external API...")
    
    try:
        # Fetch data from external API
        response = requests.get(EXTERNAL_API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        suspects_data = data.get('object', [])
        print(f"Found {len(suspects_data)} suspects in the external API.")
        
        # Process each suspect
        for suspect_data in suspects_data:
            try:
                # Extract suspect information
                full_name = suspect_data.get('full_name', '')
                nickname = suspect_data.get('nickname', '')
                nid = suspect_data.get('nid', '')
                dangerous_level = suspect_data.get('dangerous', '')
                dangerous_color = suspect_data.get('dangerous_color', '')
                photo_url = suspect_data.get('photo', '')
                
                # Skip if no photo
                if not photo_url:
                    print(f"Skipping suspect {full_name} - no photo available.")
                    continue
                
                # Download photo
                # Handle relative URLs by prepending the base API URL
                full_photo_url = photo_url
                if photo_url.startswith('/'):
                    full_photo_url = f"http://10.110.2.220:3333/api/v1/files?url={photo_url}"
                
                photo_filename = f"suspect_{suspect_data['id']}.jpg"
                photo_path = MEDIA_ROOT / photo_filename
                
                embedding = None
                if download_image(full_photo_url, photo_path):
                    # Extract face embedding
                    embedding = extract_face_embedding(photo_path)
                    if embedding is None:
                        print(f"Failed to extract face embedding for suspect {full_name}")
                        # Delete downloaded photo since we couldn't process it
                        if photo_path.exists():
                            photo_path.unlink()
                else:
                    print(f"Failed to download photo for suspect {full_name}, using random embedding")
                    # Create a random embedding for testing
                    embedding = np.random.rand(512).tolist()
                    # Create a placeholder image with the suspect's name
                    create_placeholder_image(photo_path, nickname or full_name)
                
                # Skip if we still don't have an embedding
                if embedding is None:
                    print(f"No embedding available for suspect {full_name}")
                    continue
                
                # Save to database
                suspect, created = Suspect.objects.get_or_create(
                    id=suspect_data['id'],
                    defaults={
                        'full_name': full_name,
                        'nickname': nickname,
                        'nid': nid,
                        'dangerous_level': dangerous_level,
                        'dangerous_color': dangerous_color,
                    }
                )
                
                # Update suspect with photo paths and embeddings
                suspect.set_photo_paths([photo_filename])
                suspect.set_embeddings([embedding])
                suspect.save()
                
                if created:
                    print(f"Added new suspect: {full_name}")
                else:
                    print(f"Updated existing suspect: {full_name}")
                    
            except Exception as e:
                print(f"Error processing suspect {suspect_data.get('full_name', 'Unknown')}: {e}")
                continue
                
        print("Finished populating suspects database.")
        
    except Exception as e:
        print(f"Error fetching suspects data: {e}")


if __name__ == "__main__":
    populate_suspects()