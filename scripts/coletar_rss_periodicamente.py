#!/usr/bin/env python
"""
Script para coletar notícias RSS periodicamente
"""

import os
import sys
import time
import django
from django.core.management import execute_from_command_line

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacip_backend.settings')
django.setup()

from django.core.management import call_command

def coletar_rss_periodicamente(intervalo_minutos=30):
    """
    Coleta notícias RSS a cada intervalo especificado (em minutos)
    """
    print(f"Iniciando coleta periódica de notícias RSS a cada {intervalo_minutos} minutos...")
    
    while True:
        try:
            print(f"Coletando notícias RSS em {time.strftime('%Y-%m-%d %H:%M:%S')}...")
            call_command('coletar_rss')
        except Exception as e:
            print(f"Erro ao coletar notícias: {str(e)}")
        
        # Aguardar o intervalo especificado
        time.sleep(intervalo_minutos * 60)

if __name__ == "__main__":
    # Por padrão, coletar a cada 30 minutos
    intervalo = 30
    if len(sys.argv) > 1:
        try:
            intervalo = int(sys.argv[1])
        except ValueError:
            print("Intervalo inválido. Usando padrão de 30 minutos.")
    
    coletar_rss_periodicamente(intervalo)