import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from users.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

email = 'sacip@pn.gov.ao'
password = 'sacip@1234'

try:
    user = User.objects.get(email=email)
    print(f"User found: {user.email}")
    
    # Method 1: authenticate
    auth_user = authenticate(email=email, password=password)
    print(f"authenticate(email=email, password=password): {auth_user}")
    
    # Method 2: authenticate with username
    auth_user_2 = authenticate(username=email, password=password)
    print(f"authenticate(username=email, password=password): {auth_user_2}")

    # Method 3: check_password
    pwd_match = check_password(password, user.password)
    print(f"check_password(password, user.password): {pwd_match}")
    
except User.DoesNotExist:
    print(f"User with email {email} NOT found.")
