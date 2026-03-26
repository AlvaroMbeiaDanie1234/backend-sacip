import requests
import json

urls = [
    "http://10.110.71.5:3333/api/v1/sicgo/delituosos_procurados/public/todas",
    "http://10.110.71.5:3333/api/v1/sicgo/dinfop_delitouso/public/todas",
    "http://10.110.71.5:3333/api/v1/sicgo/detido/public/todas"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
}

for url in urls:
    print(f"\nTesting {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Keys: {list(data.keys())}")
            if 'data' in data and data['data']:
                print(f"Data count: {len(data['data'])}")
                print(f"First item: {json.dumps(data['data'][0], indent=2)[:500]}")
            else:
                print("Data is empty or null")
        else:
            print(f"Error Body: {response.text[:200]}")
    except Exception as e:
        print(f"Error connect: {e}")
