import requests
import json

# Test the captures endpoint
print("=" * 60)
print("Testing captures endpoint for Suspect 1...")
print("=" * 60)

try:
    response = requests.get('http://10.110.2.30:81/api/angosite/captures/?suspect_id=1')
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print(f"\nTotal captures found: {len(data)}")
    else:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing sessions endpoint...")
print("=" * 60)

try:
    response = requests.get('http://10.110.2.30:81/api/angosite/debug/sessions/')
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print(f"\nTotal sessions found: {len(data)}")
    else:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")

# Test all captures without filter
print("\n" + "=" * 60)
print("Testing all captures (no filter)...")
print("=" * 60)

try:
    response = requests.get('http://10.110.2.30:81/api/angosite/captures/')
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    if response.status_code == 200:
        data = response.json()
        print(f"Total captures found: {len(data)}")
        if len(data) > 0:
            print("\nFirst 3 captures:")
            print(json.dumps(data[:3], indent=2))
    else:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
