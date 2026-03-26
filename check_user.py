import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from users.models import User

email = 'sacip@pn.gov.ao'
try:
    user = User.objects.get(email=email)
    print(f"User found: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Username: {user.username}")
except User.DoesNotExist:
    print(f"User with email {email} NOT found.")

# List first 5 users
print("\nFirst 5 users:")
for u in User.objects.all()[:5]:
    print(f"- {u.email} ({u.username})")
