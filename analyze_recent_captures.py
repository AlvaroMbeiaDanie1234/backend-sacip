import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from invasao.models import CapturedMedia, IntrusionSession

print("=" * 60)
print("ANÁLISE DE CAPTURAS RECENTES")
print("=" * 60)

# Check captures from last 30 minutes
now = datetime.now()
thirty_min_ago = now - timedelta(minutes=30)
one_hour_ago = now - timedelta(hours=1)
today = now.replace(hour=0, minute=0, second=0, microsecond=0)

recent_30min = CapturedMedia.objects.filter(timestamp__gte=thirty_min_ago)
recent_1hour = CapturedMedia.objects.filter(timestamp__gte=one_hour_ago)
today_captures = CapturedMedia.objects.filter(timestamp__gte=today)

print(f"\nCapturas nos últimos 30 minutos: {recent_30min.count()}")
print(f"Capturas na última hora: {recent_1hour.count()}")
print(f"Capturas hoje: {today_captures.count()}")

# Show most recent captures
print(f"\n5 Capturas mais recentes:")
print("-" * 60)
recent = CapturedMedia.objects.all().order_by('-timestamp')[:5]
for cap in recent:
    print(f"ID: {cap.id}")
    print(f"  Sessão: {cap.session.title}")
    print(f"  Tipo: {cap.media_type}")
    print(f"  Timestamp: {cap.timestamp}")
    print(f"  Há {(now - cap.timestamp.replace(tzinfo=None)).total_seconds() / 60:.1f} minutos")
    print()

print("=" * 60)
