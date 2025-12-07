# Análise de Média & OSINT

Este módulo implementa funcionalidades de Análise de Média e OSINT (Open Source Intelligence) para o sistema SACIP.

## Funcionalidades

- Pesquisa OSINT usando SerpAPI
- Análise de resultados de busca
- Coleta de informações de fontes abertas

## Configuração

Para usar este módulo, você precisa configurar a chave da API SerpAPI no arquivo de configurações do Django:

```python
SERPAPI_KEY = 'sua-chave-api-aqui'
```

## Endpoints

- `GET /api/analise-de-media-e-osint/osint-search/?q=<termo-de-busca>` - Realiza uma pesquisa OSINT

## Dependências

- requests
- django
- djangorestframework