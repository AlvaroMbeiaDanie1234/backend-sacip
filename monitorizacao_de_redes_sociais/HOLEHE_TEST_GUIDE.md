# 📧 Guia de Teste do Holehe (Email OSINT)

## ✅ Correções Implementadas

### Problema Anterior:
- ❌ O holehe funcionava no terminal mas não retornava resultados para o frontend
- ❌ Apenas mostrava "Varrendo redes sociais por e-mail" e desaparecia
- ❌ Só enviava resultados quando `exists = true` (perdendo todos os outros)

### Solução Implementada:
- ✅ **Agora envia TODOS os resultados** (encontrados e não encontrados)
- ✅ **Logging detalhado** no backend para debug
- ✅ **Interface melhor** no frontend mostrando ambos os estados
- ✅ **Contadores em tempo real** de sites verificados

## 🧪 Como Testar

### 1. Inicie o Backend
```bash
cd backend-v2
python manage.py runserver
```

### 2. Observe os Logs
Quando clicar em "Pesquisar" no frontend, deve ver no terminal:

```
🔍 Starting Holehe search for: alvaro@gmail.com
📊 Found 120 websites to check
🚀 Starting async scan of 120 websites...

🧵 Holehe thread started

   ✅ Checked twitter.com: FOUND
   ❌ Checked facebook.com: not found
   ✅ Checked github.com: FOUND
   ⏳ Progress: 10/120 websites queued...
   ...
✅ Holehe scan completed! Checked 121 websites
📦 Total results to send: 121

🏁 Holehe stream finished
```

### 3. Verifique o Frontend

No navegador, vá para:
- **Monitorização de Redes Sociais** → aba **socialScan**
- Insira um email: `alvaro@gmail.com`
- Clique em **"Pesquisar"**

Deve ver:
1. **Loading state**: "⏳ Varrendo redes sociais por e-mail..."
2. **Resultados aparecendo gradualmente** com:
   - ✅ Verde para contas encontradas
   - ❌ Cinza para contas não encontradas
3. **Contador**: "121 sites verificados | ✅ 45 encontrados"

## 📊 Exemplo de Resultados

O frontend agora mostra:

```
┌─────────────────────────────────────────────┐
│ OSINT por E-mail (holehe)                  │
├─────────────────────────────────────────────┤
│ [alvaro@gmail.com] [🔍 Pesquisar]          │
│                                             │
│ Resultados: 121 sites verificados  ✅ 45    │
│                                             │
│ ┌──────────────┬──────────────┬─────────┐  │
│ │ ✅ twitter   │ ❌ facebook  │ ✅ github│  │
│ │ twitter.com  │ facebook.com │ github.c│  │
│ ├──────────────┼──────────────┼─────────┤  │
│ │ ✅ instagram │ ❌ linkedin  │ ✅ reddit│  │
│ │ instagram.co │ linkedin.com │ reddit.c│  │
│ └──────────────┴──────────────┴─────────┘  │
└─────────────────────────────────────────────┘
```

## 🔍 Debug de Problemas

### Se não aparecerem resultados:

#### 1. Verifique o Backend
```bash
# No terminal do backend, procure por:
🔍 Starting Holehe search for: <email>
📊 Found <X> websites to check
```

#### 2. Verifique o Console do Navegador
Abra DevTools (F12) → Console e procure por:
```javascript
🏁 Holehe completed: {total_checked: 121, total_found: 45}
```

#### 3. Erros Comuns

**Erro: "ModuleNotFoundError: No module named 'trio'"**
```bash
pip install trio httpx
```

**Erro: "Holehe error: ... "**
Verifique se o módulo holehe está instalado:
```bash
cd backend-v2/monitorizacao_de_redes_sociais/holehe_tool
python -c "from holehe_tool import core; print('OK')"
```

**Erro no frontend: "Stream não disponível"**
Verifique se o backend está rodando e acessível.

## 📝 Notas Importantes

1. **Tempo de Resposta**: 
   - 120 sites levam ~10-15 segundos
   - Seja paciente durante a varredura

2. **Resultados**:
   - ✅ **Found**: Email cadastrado no site
   - ❌ **Not Found**: Email não cadastrado ou site indisponível

3. **Rate Limiting**:
   - Alguns sites podem rate limitar
   - O holehe lida com isso automaticamente

4. **Privacidade**:
   - Use apenas para investigações autorizadas
   - Respeite leis de proteção de dados

## 🎯 Próximos Passos

Se funcionar corretamente, você verá:
- ✅ Todos os 120+ sites sendo verificados
- ✅ Resultados aparecendo em tempo real
- ✅ Contador atualizando progressivamente
- ✅ Diferenciação visual entre encontrados/não encontrados

## 📞 Suporte

Se ainda tiver problemas:
1. Verifique os logs do backend
2. Abra o console do navegador (F12)
3. Execute no terminal:
   ```bash
   cd backend-v2
   python -c "from monitorizacao_de_redes_sociais.holehe_tool import core; print(core.import_submodules('monitorizacao_de_redes_sociais.holehe_tool.modules'))"
   ```

---

**Data:** 2026-03-06  
**Versão:** 3.0 - Holehe com streaming completo de resultados
