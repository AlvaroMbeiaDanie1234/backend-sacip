import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_piips_endpoints():
    # 1. Login to get token
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {"email": "sacip@pn.gov.ao", "password": "sacip@1234"}
    
    print(f"Tentando login em {login_url}...")
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code != 200:
            print(f"Falha no login: {response.status_code}")
            print(response.text)
            return
        
        token = response.json().get('token')
        print(f"Login bem sucedido! Token obtido.")
        
        headers = {"Authorization": f"Token {token}"}
        
        # 2. Test PIIPS endpoints
        endpoints = [
            "/piips/ocorrencias/",
            "/piips/delituosos-procurados/",
            "/piips/dinfop-delituoso/"
        ]
        
        for ep in endpoints:
            url = f"{BASE_URL}{ep}"
            print(f"\nTestando endpoint: {url}")
            try:
                res = requests.get(url, headers=headers, timeout=10)
                print(f"Status: {res.status_code}")
                if res.status_code == 200:
                    data = res.json()
                    print(f"Dados recebidos (primeiros 100 caracteres): {str(data)[:100]}...")
                else:
                    print(f"Erro: {res.text}")
            except Exception as e:
                print(f"Erro na requisição: {e}")
                
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

if __name__ == "__main__":
    test_piips_endpoints()
