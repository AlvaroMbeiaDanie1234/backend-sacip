import threading
from django.apps import AppConfig
import sys

class FacialRecognitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facial_recognition'

    def ready(self):
        # Avoid running on migration or import commands
        if 'runserver' not in sys.argv:
            return
            
        from .views import initialize_face_app, scan_media_directories
        
        def warmup():
            print("🚀 Starting Facial Recognition warmup...")
            initialize_face_app()
            scan_media_directories()
            print("✅ Facial Recognition warmup complete!")

        # Run in a separate thread to not block startup
        thread = threading.Thread(target=warmup)
        thread.daemon = True
        thread.start()
