# Resolução do Erro "cms" no socialScan

## Problema Identificado

O erro **"cms"** que ocorria durante a varredura de redes sociais na aba **socialScan** estava relacionado com:

1. **Proteção Anti-Bot/CMS**: Sites protegidos por CMS (WordPress, Drupal, etc.) ou sistemas anti-bot (Cloudflare, Akamai) estavam a bloquear o scraping
2. **Falta de resiliência**: Um erro num perfil parava toda a varredura da plataforma
3. **Logging insuficiente**: Não era possível diagnosticar onde estava a falhar

## Melhorias Implementadas

### 1. ✅ Detecção de Bloqueios por CMS/Anti-Bot

O sistema agora detecta e reporta quando encontra:
- Páginas de "Access Denied"
- Erros "403 Forbidden"
- CAPTCHAs
- Protecção Cloudflare/Akamai
- Outros mecanismos anti-bot

**Código adicionado em `scraper.py`:**
```python
# Check for common CMS error pages or access denied
page_title = self.webdriver.title.lower() if self.webdriver.title else ""
if any(term in page_title for term in ['access denied', '403 forbidden', '404 not found', 'captcha', 'blocked']):
    print(f"⚠️  Blocked by CMS or anti-bot protection at {url}")
    return None
```

### 2. ✅ Resiliência Melhorada - Um Erro Não Para Tudo

Antes: Se um perfil falhasse, toda a varredura parava.

Agora: O sistema continua a varrer os outros perfis mesmo quando um falha.

**Exemplo no método `scrape_by_platform`:**
```python
for i, perfil in enumerate(perfis, 1):
    try:
        result = self.scrape_profile_and_posts(perfil.id, limit)
        # Process result...
    except Exception as e:
        error_count += 1
        print(f"\n❌ Error processing profile {perfil.nome_usuario}: {str(e)}")
        # Continue with next profile - don't let one failure stop the whole scan
```

### 3. ✅ Logging Detalhado com Emojis

Cada passo do processo agora é registado com emojis e mensagens claras:
- 🔄 Início da sincronização
- 📊 Quantidade de dados encontrados
- ✅ Sucesso nas operações
- ⚠️ Avisos e problemas não críticos
- ❌ Erros críticos

**Exemplo de output:**
```
================================================================================
🚀 Starting complete sync for Profile ID: 5
================================================================================

📋 Step 1: Syncing profile data...
🔄 Starting profile sync for john_doe on twitter...
   🐦 Scraping Twitter posts from https://twitter.com/john_doe...
   📊 Found 15 tweets on page
   ✅ Extracted 10 posts from Twitter
✅ Profile synced successfully for john_doe

📝 Step 2: Syncing posts...
📥 Starting post sync for john_doe on twitter (limit: 10)...
📊 Found 10 posts to process
   ↳ Added 5 new posts so far...
✅ Successfully added 7 new posts for john_doe

================================================================================
✅ Complete sync finished for Profile ID: 5
   - Profile synced: True
   - New posts found: 7
================================================================================
```

### 4. ✅ Mensagens de Erro Mais Claras no Frontend

O frontend agora mostra mensagens informativas:
- 🔄 "Iniciando varredura..."
- ✅ "Sucesso: 15 novas postagens encontradas"
- ⚠️ "Varredura parcial: 5 posts encontrados. Aviso: Rate limit detected"
- ℹ️ "Nenhuma nova postagem encontrada"
- ❌ "Erro na varredura: Detalhes do erro"

### 5. ✅ Tratamento de Erros em Cascata

Cada camada (scraper → service → view → frontend) agora:
1. Captura erros explicitamente
2. Regista o erro com detalhes
3. Retorna informação útil ao utilizador
4. Permite continuar operações possíveis

## Como Testar

### No Backend (Terminal):
```bash
cd backend-v2
python manage.py runserver
```

Observe os logs detalhados quando fizer scraping.

### No Frontend:
1. Aceda à página **Monitorização de Redes Sociais**
2. Vá à aba **socialScan**
3. Clique em **"Atualizar"** num perfil
4. Observe as mensagens de status com emojis

## Solução de Problemas Comuns

### Problema: "Blocked by CMS or anti-bot protection"

**Causa:** O site tem proteção Cloudflare, Akamai ou similar

**Soluções:**
1. Use proxies diferentes (configurar em `settings.py`)
2. Aumente o delay entre requests
3. Use contas autenticadas (login) se possível
4. Considere usar APIs oficiais quando disponíveis

### Problema: "Rate Limit detected"

**Causa:** Muitas requisições em pouco tempo

**Soluções:**
1. Aguarde alguns minutos antes de tentar novamente
2. O sistema já implementa rate limiting automático
3. Reduza o número de perfis varridos de uma vez

### Problema: Timeout na varredura

**Causa:** Perfil indisponível ou rede lenta

**Soluções:**
1. Verifique sua conexão com a internet
2. O perfil pode ter sido removido ou tornado privado
3. Aumente o timeout em `scraper.py` se necessário

## Próximos Passos Sugeridos

1. **Configurar Proxy Rotation**: Adicione proxies em `settings.py` para melhor anonimato
2. **Implementar Login Automático**: Para perfis privados/autenticados
3. **Adicionar Cache**: Evitar re-scraping de conteúdo já coletado
4. **Dashboard de Status**: Mostrar estatísticas de sucesso/erro por plataforma

## Ficheiros Modificados

- `backend-v2/monitorizacao_de_redes_sociais/scraper.py` ✅
- `backend-v2/monitorizacao_de_redes_sociais/views.py` ✅
- `frontend-v2/sistema-de-intelig-ncia-policial/app/redes-sociais/page.tsx` ✅

## Notas Importantes

- ⚠️ **Não faça scraping de perfis privados sem autorização**
- ⚠️ **Respeite os termos de serviço de cada plataforma**
- ⚠️ **Use rate limiting para não sobrecarregar os servidores**
- ⚠️ **Este sistema é para uso ético e legal apenas**

---

**Data da atualização:** 2026-03-06  
**Versão:** 2.0 - Com tratamento robusto de erros CMS
