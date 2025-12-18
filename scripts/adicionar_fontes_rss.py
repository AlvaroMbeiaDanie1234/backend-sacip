#!/usr/bin/env python
"""
Script para adicionar fontes RSS de exemplo ao banco de dados
"""

import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from servico_rss.models import FonteRSS
from users.models import User

def adicionar_fontes_exemplo():
    # Verificar se já existem fontes RSS
    if FonteRSS.objects.exists():
        print("Já existem fontes RSS no banco de dados.")
        return

    # Obter um usuário para associar às fontes (você pode modificar isso conforme necessário)
    try:
        usuario = User.objects.first()
        if not usuario:
            print("Nenhum usuário encontrado. Crie um usuário primeiro.")
            return
    except User.DoesNotExist:
        print("Nenhum usuário encontrado. Crie um usuário primeiro.")
        return

    # Fontes RSS de exemplo (você pode adicionar mais ou modificar estas)
    fontes_exemplo = [
        {
            "nome": "BBC News",
            "url": "http://feeds.bbci.co.uk/news/rss.xml",
            "descricao": "Últimas notícias da BBC"
        },
        {
            "nome": "CNN",
            "url": "http://rss.cnn.com/rss/edition.rss",
            "descricao": "Notícias internacionais da CNN"
        },
        {
            "nome": "TechCrunch",
            "url": "https://techcrunch.com/feed/",
            "descricao": "Notícias sobre tecnologia e startups"
        }
    ]

    # Adicionar fontes ao banco de dados
    for fonte_data in fontes_exemplo:
        fonte, created = FonteRSS.objects.get_or_create(
            url=fonte_data["url"],
            defaults={
                "nome": fonte_data["nome"],
                "descricao": fonte_data["descricao"],
                "adicionado_por": usuario
            }
        )
        
        if created:
            print(f"Fonte RSS '{fonte.nome}' adicionada com sucesso.")
        else:
            print(f"Fonte RSS '{fonte.nome}' já existe.")

    print("Processo de adição de fontes RSS concluído.")

if __name__ == "__main__":
    adicionar_fontes_exemplo()