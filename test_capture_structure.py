import requests
import json

# Test the captures endpoint for suspect 489
print("=" * 60)
print("Testing captures endpoint for Suspect 489...")
print("=" * 60)

try:
    response = requests.get('http://127.0.0.1:8000/api/angosite/captures/?suspect_id=489')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal captures found: {len(data)}")
        
        if len(data) > 0:
            print("\nFirst capture structure:")
            print(json.dumps(data[0], indent=2))
            
            print("\nAll fields in first capture:")
            for key, value in data[0].items():
                print(f"  {key}: {type(value).__name__} = {value}")
        else:
            print("No captures found")
    else:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
