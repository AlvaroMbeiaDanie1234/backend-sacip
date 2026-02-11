import cv2
import base64
import numpy as np
import json
import os
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Suspect, CameraFeed, RecognitionResult, Alert
from .serializers import SuspectSerializer, CameraFeedSerializer, RecognitionResultSerializer, AlertSerializer

# Import InsightFace
try:
    from insightface.app import FaceAnalysis
    INSIGHTFACE_AVAILABLE = True
except ImportError:
    INSIGHTFACE_AVAILABLE = False
    print("InsightFace not available. Facial recognition will be disabled.")

# Configuration
MODEL_NAME = 'buffalo_l'
THRESHOLD = 0.0

# Initialize FaceAnalysis (deferred until needed)
face_app = None
face_app_initialized = False


def initialize_face_app():
    """Initialize the face analysis app if not already initialized."""
    global face_app, face_app_initialized
    
    if not INSIGHTFACE_AVAILABLE:
        return False
    
    if not face_app_initialized:
        face_app = FaceAnalysis(name=MODEL_NAME, providers=['CPUExecutionProvider'], root=Path("models"))
        face_app.prepare(ctx_id=0, det_size=(640, 640))
        face_app_initialized = True
        print("✅ Face analysis model initialized")
        
    return face_app is not None


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def load_suspects_database():
    """Load suspects with their face embeddings from the database."""
    suspects_db = []
    suspects = Suspect.objects.all()
    
    for suspect in suspects:
        embeddings = suspect.get_embeddings()
        photo_paths = suspect.get_photo_paths()
        
        # Get the first photo path if available
        photo_url = ""
        if photo_paths and isinstance(photo_paths, list) and len(photo_paths) > 0:
            # Generate Django media URL for the photo
            photo_url = f"/media/{photo_paths[0]}"
        
        if embeddings:
            # Assuming the first embedding for simplicity
            suspects_db.append({
                'id': suspect.id,
                'full_name': suspect.full_name,
                'nickname': suspect.nickname,
                'dangerous_level': suspect.dangerous_level,
                'dangerous_color': suspect.dangerous_color,
                'photo_url': photo_url,
                'embedding': np.array(embeddings[0]) if isinstance(embeddings[0], list) else embeddings[0],
                'suspect_obj': suspect
            })
    
    return suspects_db


def extract_faces_from_image(image_path):
    """Extract face embeddings from an image file."""
    if not INSIGHTFACE_AVAILABLE:
        return []
    
    # Initialize face app if not already done
    if not initialize_face_app():
        return []
    
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"⚠️ Could not load image: {image_path}")
            return []
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect faces in the image
        faces = face_app.get(img_rgb)
        
        face_data = []
        for face in faces:
            embedding = face.embedding
            bbox = face.bbox.astype(int)
            
            face_data.append({
                'embedding': embedding,
                'bbox': bbox,
                'image_path': image_path
            })
        
        return face_data
    except Exception as e:
        print(f"Error extracting faces from {image_path}: {e}")
        return []


# Global cache for media face data
MEDIA_FACES_CACHE = None

def scan_media_directories(force_refresh=False):
    """Scan media directories for images to use in facial recognition."""
    global MEDIA_FACES_CACHE
    
    # Return cached data if available and not forcing refresh
    if MEDIA_FACES_CACHE is not None and not force_refresh:
        # print(f"✅ Using cached media faces ({len(MEDIA_FACES_CACHE)} faces)")
        return MEDIA_FACES_CACHE

    print("🔄 Scanning media directories for faces...")
    media_dirs = [
        "",  # Main media directory (relative to MEDIA_ROOT)
        "invasion_media",  # Invasion media directory
        "suspicious_info_photos"  # Suspicious information photos directory
    ]
    
    all_face_data = []
    
    for media_dir in media_dirs:
        abs_media_dir = Path(settings.MEDIA_ROOT) / media_dir
        
        if not abs_media_dir.exists():
            print(f"⚠️ Media directory does not exist: {abs_media_dir}")
            continue
        
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        for root, dirs, files in os.walk(abs_media_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in image_extensions:
                    try:
                        face_data = extract_faces_from_image(str(file_path))
                        for face in face_data:
                            face['id'] = str(file_path)
                            face['source'] = 'Base de dados da POLICIA NACIONAL'
                            media_root = Path(settings.MEDIA_ROOT)
                            try:
                                relative_path = file_path.relative_to(media_root)
                                relative_path_str = str(relative_path).replace('\\', '/')
                            except ValueError:
                                relative_path = file_path.relative_to(Path(os.getcwd()))
                                relative_path_str = str(relative_path).replace('\\', '/')
                            face['photo_url'] = f"/media/{relative_path_str}"
                            
                            # print(f"Generated photo URL: {face['photo_url']} for file: {file_path}")
                            all_face_data.append(face)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
    
    print(f"🔍 Found {len(all_face_data)} faces in media directories")
    MEDIA_FACES_CACHE = all_face_data
    return all_face_data


def recognize_suspects(embedding, suspects_db, threshold=THRESHOLD, media_face_data=None, min_similarity=0.5):
    """Recognize suspects based on face embedding."""
    results = []
    
    for suspect in suspects_db:
        similarity = cosine_similarity(embedding, suspect['embedding'])
        print(f"🔍 Comparing with {suspect['nickname']}: similarity = {similarity:.2f}")
        
        if similarity > threshold and similarity >= min_similarity:
            results.append({
                "id": suspect['id'],
                "full_name": suspect['full_name'],
                "nickname": suspect['nickname'],
                "dangerous_level": suspect['dangerous_level'],
                "dangerous_color": suspect['dangerous_color'],
                "similarity": float(similarity),
                "photo_url": suspect.get('photo_url', ''),  # This should now contain proper media URLs
                "source": "Base de dados Policial",
                "suspect_obj": suspect['suspect_obj']
            })
    
    if media_face_data:
        for face_data in media_face_data:
            similarity = cosine_similarity(embedding, face_data['embedding'])
            print(f"🔍 Comparing with media image {face_data['id']}: similarity = {similarity:.2f}")
            
            # Return all faces that meet the similarity threshold
            if similarity > threshold and similarity >= min_similarity:
                results.append({
                    "id": face_data['id'],
                    "full_name": f"Imagem de {os.path.basename(face_data['image_path'])}",
                    "nickname": f"{os.path.basename(face_data['image_path'])}",
                    "dangerous_level": "N/A",
                    "dangerous_color": "#808080",
                    "similarity": float(similarity),
                    "photo_url": face_data.get('photo_url', ''),  # This contains the media URL
                    "source": face_data.get('source', 'Base de dados da POLICIA NACIONAL'),
                    "suspect_obj": None  # No database object for media images
                })
    
    # Sort results by similarity (highest first)
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    if results:
        best_match = results[0]
        print(f"✅ Best match: {best_match['nickname']} ({best_match['similarity']:.2f})")
    
    return results


@csrf_exempt
def process_frame(request):
    """Process a video frame for facial recognition."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    if not INSIGHTFACE_AVAILABLE:
        return JsonResponse({'error': 'Facial recognition is not available'}, status=500)
    
    try:
        data = json.loads(request.body)
        frame_data = data.get('frame')
        camera_id = data.get('camera_id', 1)  # Default to camera 1 if not specified
        
        if not frame_data:
            return JsonResponse({'error': 'No frame data provided'}, status=400)
        
        # Decode base64 frame data
        frame_bytes = base64.b64decode(frame_data)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            return JsonResponse({'error': 'Invalid frame data'}, status=400)
        
        # Get minimum similarity threshold from request (default to 0.5 if not provided)
        min_similarity = float(data.get('min_similarity', 0.5))
        
        # Initialize face app if not already done
        if not initialize_face_app():
            return JsonResponse({'error': 'Facial recognition is not available'}, status=500)
        
        # Load suspects database
        suspects_db = load_suspects_database()
        
        # Scan media directories for additional images
        media_face_data = scan_media_directories()
        
        # Get camera feed
        try:
            camera_feed = CameraFeed.objects.get(id=camera_id)
        except CameraFeed.DoesNotExist:
            camera_feed = CameraFeed.objects.first() or CameraFeed.objects.create(
                name="Default Camera",
                location="Unknown"
            )
        
        # Detect faces in the frame
        faces = face_app.get(frame)
        print(f"🔍 Faces detected: {len(faces)}")
        
        results = []
        for face in faces:
            bbox = face.bbox.astype(int)
            embedding = face.embedding
            
            # Recognize suspects from both database and media directories with specified minimum similarity
            matches = recognize_suspects(embedding, suspects_db, media_face_data=media_face_data, min_similarity=min_similarity)
            
            for match in matches:
                # Only create alerts and results for matches above threshold from database suspects
                if match['similarity'] >= THRESHOLD and match.get('suspect_obj'):
                    # Save recognition result only for database suspects (not media directory images)
                    recognition_result = RecognitionResult.objects.create(
                        suspect=match['suspect_obj'],
                        camera_feed=camera_feed,
                        similarity_score=match['similarity'],
                        frame_data=frame_data
                    )
                    
                    # Create alert for recognized suspect
                    alert = Alert.objects.create(
                        suspect=match['suspect_obj'],
                        camera_feed=camera_feed,
                        similarity_score=match['similarity']
                    )
                
                # Only add results with similarity >= 0.5 (50%) to reduce noise
                if match["similarity"] >= 0.5:
                    results.append({
                        "id": match["id"],
                        "full_name": match["full_name"],
                        "nickname": match["nickname"],
                        "dangerous_level": match["dangerous_level"],
                        "dangerous_color": match["dangerous_color"],
                        "similarity": match["similarity"],
                        "photo_url": match.get("photo_url", ""),  # Add photo URL to results, with fallback to empty string
                        "source": match.get("source", "Base de dados Policial"),  # Add source information
                        "bbox": bbox.tolist()
                    })
                
                # Draw circle around face and label on frame
                color = (0, 255, 0)  # Green
                # Calculate center and radius for circle based on bounding box
                center_x = int((bbox[0] + bbox[2]) / 2)
                center_y = int((bbox[1] + bbox[3]) / 2)
                radius = int(max(bbox[2] - bbox[0], bbox[3] - bbox[1]) / 2)
                cv2.circle(frame, (center_x, center_y), radius, color, 2)
                
                # Draw similarity text above the circle
                cv2.putText(frame, f"{match['nickname']} ({match['similarity']:.2f})",
                           (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Draw additional info below the circle
                cv2.putText(frame, f"{match['full_name']} | {match['dangerous_level']}",
                           (bbox[0], bbox[3] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Encode processed frame back to base64
        _, buffer = cv2.imencode(".jpg", frame)
        processed_frame = base64.b64encode(buffer).decode("utf-8")
        
        print(f"📤 Sending frame: {len(processed_frame)} bytes, {len(results)} suspects")
        
        # Prepare response data
        response_data = {
            "frame": processed_frame,
            "suspects": results
        }
        
        # Return JSON response with proper headers to prevent timeout issues
        response = JsonResponse(response_data)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"
        
        return response
        
    except Exception as e:
        print(f"Error processing frame: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# DRF Views
class SuspectListView(generics.ListCreateAPIView):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer
    permission_classes = [AllowAny]


class SuspectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer
    permission_classes = [AllowAny]


class CameraFeedListView(generics.ListCreateAPIView):
    queryset = CameraFeed.objects.all()
    serializer_class = CameraFeedSerializer
    permission_classes = [AllowAny]


class CameraFeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CameraFeed.objects.all()
    serializer_class = CameraFeedSerializer
    permission_classes = [AllowAny]


class RecognitionResultListView(generics.ListCreateAPIView):
    queryset = RecognitionResult.objects.all()
    serializer_class = RecognitionResultSerializer
    permission_classes = [AllowAny]


class RecognitionResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecognitionResult.objects.all()
    serializer_class = RecognitionResultSerializer
    permission_classes = [AllowAny]


class AlertListView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]


class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]


class UnreadAlertsView(generics.ListAPIView):
    queryset = Alert.objects.filter(is_read=False)
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]