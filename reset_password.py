import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from users.models import User
from django.contrib.auth import authenticate

email = 'sacip@pn.gov.ao'
password = 'sacip@1234'

try:
    user = User.objects.get(email=email)
    print(f"User found: {user.email}")
    user.set_password(password)
    user.save()
    print(f"Password reset successfully for {email}")
    
    # Verify authentication immediately
    auth_user = authenticate(email=email, password=password)
    if auth_user:
        print(f"Verification SUCCESS: authenticate works for {email}")
    else:
        print(f"Verification FAILED: authenticate returned None after password reset.")
        
except User.DoesNotExist:
    print(f"User with email {email} NOT found.")
except Exception as e:
    print(f"Error resetting password: {str(e)}")
