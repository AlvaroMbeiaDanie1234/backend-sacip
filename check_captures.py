import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from invasao.models import CapturedMedia, IntrusionSession

# Check specifically for Suspect 1
suspect_id = '1'
print(f"Checking for Suspect {suspect_id}...")

sessions = IntrusionSession.objects.filter(title__icontains=f"Suspect {suspect_id}")
print(f"Found {sessions.count()} sessions matching 'Suspect {suspect_id}'")

for session in sessions:
    print(f"Session ID: {session.id}, Title: '{session.title}', Captures: {session.captured_media.count()}")

print("\nRecent Captures:")
captures = CapturedMedia.objects.all().order_by('-timestamp')[:5]
for c in captures:
    print(f"ID: {c.id}, Session: {c.session.title}, Type: {c.media_type}")
