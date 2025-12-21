# SACIP Backend - Sistema de Apoio à Criminalidade e Investigação Policial

## Descrição
Este é um backend completo desenvolvido em Django para o sistema SACIP, que oferece suporte a operações policiais de investigação e monitoramento.

## Arquitetura
O projeto segue uma arquitetura limpa (clean architecture) e está organizado em módulos independentes:

### Módulos
1. **users** - Gestão de usuários e autenticação
2. **informacoes_suspeitas** - Gestão de informações suspeitas
3. **alvos_sob_investigacao** - Gestão de alvos sob investigação
4. **power_bi** - Integração com dashboards Power BI
5. **consulta_de_documentos** - Consulta e gestão de documentos
6. **monitoramento_de_viaturas** - Monitoramento de viaturas em tempo real
7. **monitorizacao_de_redes_sociais** - Monitorização de perfis em redes sociais
8. **criminalidade** - Registo e análise de ocorrências criminais
9. **monitor_sos** - Gestão de chamadas de emergência SOS
10. **cruzamento_de_dados** - Ferramentas de cruzamento de dados
11. **i2_analysis_notebook** - Notebooks de análise I2
12. **relatorios** - Geração e agendamento de relatórios
13. **configuracoes** - Configurações do sistema e auditoria

## Tecnologias Utilizadas
- Django 5.2
- Django REST Framework
- Swagger (drf-yasg) para documentação da API
- SQLite (banco de dados padrão, pode ser alterado)

## Instalação

1. Criar ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Instalar dependências:
   ```
   pip install -r requirements.txt
   ```

3. Aplicar migrações:
   ```
   python manage.py migrate
   ```

4. Criar superusuário:
   ```
   python manage.py createsuperuser
   ```


   python manage.py seed_organizational_units

5. Executar servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

## Acesso às Interfaces

- **Administração**: http://127.0.0.1:8000/admin/
- **Documentação da API (Swagger)**: http://127.0.0.1:8000/swagger/
- **Documentação da API (Redoc)**: http://127.0.0.1:8000/redoc/

## Autenticação

O sistema suporta diferentes níveis de permissão:
- **Operador**: Acesso básico às funcionalidades
- **Chefe**: Acesso a funcionalidades de supervisão
- **Admin**: Acesso administrativo completo
- **Super Admin**: Acesso total ao sistema

## Estrutura de Permissões

Cada usuário pode ter múltiplos papéis atribuídos, permitindo uma flexibilidade completa no controle de acesso.

## Licença
Este projeto é destinado exclusivamente para uso pelas autoridades policiais e não deve ser distribuído publicamente.


Templates de invasão
http://127.0.0.1:8000/api/invasao/

http://127.0.0.1:8000/api/invasao/football/

http://127.0.0.1:8000/api/invasao/adult/

http://127.0.0.1:8000/api/invasao/news/

http://127.0.0.1:8000/api/invasao/prizes/

