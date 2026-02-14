import requests
import json

url = "http://127.0.0.1:8000/monitorizacao-redes-sociais/sherlock/"
data = {"username": "testuser"}

# Note: This might fail if auth is required, but I'll try to see if it even reaches the logic
# If it returns 401/403, I'll know it's blocked by auth.
# If it returns 500, I'll see the error message I added.

try:
    # First, try without auth to see if we get the 500 or 403
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response (text): {response.text[:500]}")
except Exception as e:
    print(f"Request failed: {e}")
