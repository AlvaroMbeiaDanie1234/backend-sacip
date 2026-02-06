# Updates para a Secção de Monitorização de Redes Sociais

## Alterações Requeridas

Na secção de **Monitorização de Redes Sociais**, as abas devem ser alteradas conforme abaixo:

### Abas Actuais:
- Atividade Recente
- Perfis Monitorizados  
- Google Alertas + RSS

### Novas Abas (após implementação):
- Atividade Recente
- Perfis Monitorados
- Nossa Comunidade (nova aba)

### Removidas:
- Google Alertas + RSS (será removida)

## Endpoint para a Nova Aba "Nossa Comunidade"

### Endpoint:
`GET /monitorizacao-de-redes-sociais/nossa-comunidade/users/`

### Headers:
```
Authorization: Token {user_token}
Content-Type: application/json
```

### Resposta Esperada:
```json
{
  "success": true,
  "collection": "users",
  "count": 3,
  "data": [
    {
      "id": "hWu861gV66a0cUuaDehWKujdXdY2",
      "nome": "Álvaro Mbeia Daniel Miguel",
      "email": "alvarombeiadanielmiguel@gmail.com",
      "fotoPerfil": "http://192.168.1.125:9000/nossacomunidade/user_photos/hWu861gV66a0cUuaDehWKujdXdY2/user_photos/hWu861gV66a0cUuaDehWKujdXdY2/profile.png",
      "bio": null,
      "morada": "Luanda",
      "dataNascimento": "2000-10-10T00:00:00.000",
      "lastActive": "2026-01-24T17:39:30Z",
      "fcmToken": "dNN0RPunSgOAEW7FkOX8xr:APA91bGJfBDkrlj595lu9KOTEg05mgZbfAjKd0YaCZRAAGknXsfJGECqdUnlCm-A8MNSqXVQMigfSKdT8Tp3RJ2HlL5ssOB5HjVhbcL9WooyGP9chyWiYkU",
      "telefone": "",
      "photos": [],
      "statuses": []
    }
  ]
}
```

### Campos Disponíveis para Visualização:
- `nome`: Nome completo do utilizador
- `email`: Email do utilizador
- `fotoPerfil`: URL da foto de perfil
- `bio`: Biografia do utilizador (pode ser null)
- `morada`: Localização/residência do utilizador
- `dataNascimento`: Data de nascimento (formato ISO)
- `lastActive`: Última actividade (timestamp)
- `photos`: Lista de fotos do utilizador
- `statuses`: Estados/disponibilidade do utilizador

## Implementação Frontend

### Componente React Sugerido:
```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

function NossaComunidadeTab() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchNossaComunidadeUsers();
  }, []);

  const fetchNossaComunidadeUsers = async () => {
    try {
      const token = localStorage.getItem('token'); // ou como for gerido o token
      
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/monitorizacao-de-redes-sociais/nossa-comunidade/users/`,
        {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.success) {
        setUsers(response.data.data);
      }
    } catch (err) {
      setError('Erro ao carregar utilizadores da comunidade');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Carregando membros da comunidade...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="nossa-comunidade-container">
      <h2>Membros da Nossa Comunidade ({users.length})</h2>
      <div className="users-grid">
        {users.map(user => (
          <div key={user.id} className="user-card">
            <img 
              src={user.fotoPerfil || '/default-avatar.png'} 
              alt={user.nome}
              className="user-avatar"
            />
            <div className="user-info">
              <h3>{user.nome}</h3>
              <p className="user-email">{user.email}</p>
              <p className="user-location">{user.morada}</p>
              <p className="user-bio">{user.bio || 'Sem biografia'}</p>
              <div className="user-stats">
                <span>Fotos: {user.photos?.length || 0}</span>
                <span>Estados: {user.statuses?.length || 0}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default NossaComunidadeTab;
```

## Notas Importantes

1. O endpoint faz parte do módulo de monitorização de redes sociais mas traz dados do Firestore
2. Os dados são protegidos e requerem autenticação válida
3. A estrutura dos dados pode variar dependendo do conteúdo disponível no Firestore
4. Certifique-se de tratar correctamente valores nulos (como `bio: null`)
5. As datas estão no formato ISO 8601 e podem precisar de formatação para exibição