# Cantina Interativa API

Este documento apresenta uma descrição técnica e acadêmica da arquitetura, organização de código, rotas e práticas adotadas no repositório "Cantina Interativa API". O objetivo é fornecer uma visão detalhada e prescritiva do projeto para desenvolvedores, avaliadores e equipes de manutenção.

## Resumo

Projeto RESTful construído com FastAPI e SQLAlchemy, organizado com separação clara entre camadas: rotas (API), schemas (validação), models (persistência), services (regras de negócio) e core (configuração, segurança e inicialização do banco). Testes automatizados (pytest) cobrem saúde da API, integração com banco, fluxo de cadastro e autenticação JWT.

## Arquitetura e princípios

- Estrutura modular e em camadas para promover coesão e reduzir acoplamento.
- Serviços (`app/services`) concentram regras de negócio, evitando lógica nas rotas (princípio DRY).
- Dependências (DB, autenticação) são explicitadas via `Depends` do FastAPI e sobrescritas nos testes para isolamento.
- Testes automatizados e fixtures garantem reprodutibilidade dos resultados e ambiente controlado.

## Estrutura do repositório (visão por arquivo/diretório)

- `main.py`: Ponto de entrada da aplicação. Configura o `FastAPI`, middleware e registra os routers. (Veja [main.py](main.py)).
- `app/core/config.py`: Configurações centrais do projeto (paths, URL do banco). (Veja [app/core/config.py](app/core/config.py)).
- `app/core/database.py`: Engine SQLAlchemy, `SessionLocal`, `Base`, e função `init_db()` que cria tabelas em desenvolvimento. (Veja [app/core/database.py](app/core/database.py)).
- `app/core/security.py`: Funções de hashing de senha e criação/verificação de JWT. Atualmente contém `SECRET_KEY` e `ALGORITHM` hardcoded para desenvolvimento — recomenda-se migração para variáveis de ambiente. (Veja [app/core/security.py](app/core/security.py)).
- `app/models/`: Modelos ORM (`Usuario`, `Cliente`, `Produto`) que definem a estrutura persistida no banco. (Ex.: [app/models/usuarios.py](app/models/usuarios.py)).
- `app/schemas/`: Schemas Pydantic para validação de entrada/saída (ex.: `UsuarioCreate`, `UsuarioRead`). (Ex.: [app/schemas/usuario.py](app/schemas/usuario.py)).
- `app/api/v1/`: Routers versionados. Contém `auth.py` (login), `routers/usuarios.py`, `routers/clientes.py`, `routers/produtos.py`. Os routers apenas expõem endpoints e delegam lógica a services.
- `app/services/`: Nova camada introduzida para concentrar regras de negócio e operações complexas. Ex.: `app/services/usuarios_service.py` contém `create_user` e `authenticate_user`.
- `alembic/`: Migrations do banco. Possui scripts de versões e configuração do Alembic para migrações controladas.
- `tests/` e `test_api.py`, `tests/test_integration.py`: Testes de unidade e integração. `conftest.py` define fixtures para criação de um banco SQLite de teste isolado e override de dependências.

### Árvore hierárquica do repositório

Segue uma representação em árvore do repositório para rápida visualização da arquitetura e das responsabilidades por pasta/arquivo:

```
.
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── README
│   └── versions/
│       ├── 079bca24c680_add_is_admin_to_users.py
│       ├── 9cb6b83a6096_cria_tabela_de_usuarios.py
│       └── ...
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── deps.py
│   │       └── routers/
│   │           ├── __init__.py
│   │           ├── clientes.py
│   │           ├── produtos.py
│   │           └── usuarios.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── cliente.py
│   │   ├── produto.py
│   │   └── usuarios.py
│   ├── schemas/
│   │   ├── cliente.py
│   │   ├── produto.py
│   │   └── usuario.py
│   └── services/
│       └── usuarios_service.py
├── tests/
│   ├── test_app.py
│   └── test_integration.py
├── conftest.py
├── main.py
├── README.md
└── requirements.txt
```

## Rotas principais e comportamento esperado

- `GET /health` — verifica se a API está operacional.
- `POST /api/v1/usuarios/` — registra um novo usuário. Entrada: `UsuarioCreate` (email, password, nome_completo, is_active). Resposta: `UsuarioRead` (id, email, ...). Retorna `400` se email já existir.
- `POST /api/v1/auth/login` — autenticação via `OAuth2PasswordRequestForm` (username=email, password). Retorna `access_token` JWT e `token_type`.
- `GET/POST/PUT/DELETE /api/v1/clientes` — CRUD para clientes (implementados em `app/api/v1/routers/clientes.py`).
- `GET/POST/PUT/DELETE /api/v1/produtos` — CRUD para produtos (implementados em `app/api/v1/routers/produtos.py`).

As rotas de negócio delegam validações e persistência para `services` e `models` respectivamente, preservando os routers enxutos e sem lógica de negócio.

## Mudanças relevantes e motivação (refatorações aplicadas)

- Introdução da camada `services` (`app/services/usuarios_service.py`): centraliza criação e autenticação de usuários; facilita testes unitários e evita duplicação de código nas rotas.
- Correção de `conftest.py`: antes, um arquivo de banco `test_db.db` persistente causava falsos-positivos/falhas nos testes. Agora o arquivo é removido antes da criação do engine de teste e a fixture sobrescreve explicitamente o `get_db` utilizado pelos routers (`app.api.v1.deps.get_db`). Isso garante isolamento entre execuções.
- Substituição de importações relativas de profundidade crítica por importações absolutas (`app.services...`) para evitar erros de importação quando o pacote é executado como módulo de teste.

## Problemas encontrados e como foram mitigados (troubleshooting)

- Problema: Falha intermitente no teste de cadastro (`HTTP 400`) devido a banco de testes com dados residuais.
	- Mitigação: Remoção do arquivo `test_db.db` no início dos testes em `conftest.py` e isolamento das transações por fixture.

- Problema: `ImportError: attempted relative import beyond top-level package` após mover arquivos e criar `services`.
	- Mitigação: Adoção de importações absolutas (`from app.services...`) em módulos do pacote; garante compatibilidade com execução via `pytest` e execução direta.

- Problema: Tentativas de ativação do virtualenv via PowerShell encontravam políticas de execução restritas em alguns ambientes.
	- Mitigação: nos comandos de exemplo é recomendado chamar diretamente o executável do venv `./.venv/Scripts/python.exe -m pytest` para evitar a necessidade de alterar políticas locais.

## Testes

- Executar todos os testes (recomendado usar o Python do venv):

```powershell
& ".venv/Scripts/python.exe" -m pytest -q
```

- Testes importantes introduzidos:
	- `tests/test_integration.py`: valida conexão com o banco, fluxo de cadastro de usuário e verificação do JWT.
	- `tests/test_app.py` e `test_api.py`: checagens de health e proteção de rota de produtos sem autenticação.

## Como executar localmente (desenvolvimento)

1. Crie e ative um ambiente virtual (Windows Powershell):

```powershell
python -m venv .venv
& ".venv/Scripts/Activate.ps1"
pip install -r requirements.txt
```

2. Crie o arquivo de ambiente local com o modelo fornecido:

```powershell
copy .env.example .env
```

3. Ajuste `.env` com os valores apropriados para o ambiente de desenvolvimento.

4. Criar/migrar o banco de dados (opcional em desenvolvimento):

```bash
alembic upgrade head
# ou simplesmente permitir que init_db() crie as tabelas em desenvolvimento
```

5. Executar a aplicação (desenvolvimento):

```bash
uvicorn cantina_api.main:app --reload --host 127.0.0.1 --port 8000
```

6. Documentação interativa disponível em `/docs` e `/redoc`.

## Deploy para Render ou Fly.io

A aplicação está preparada para deploy em Render ou Fly.io usando Docker, com suporte a `PORT` e `DATABASE_URL`.

O repositório também inclui um `render.yaml` para automatizar a configuração do serviço no Render, reduzindo a necessidade de ajuste manual no painel.

1. Gere o arquivo de configuração local `.env`:

```bash
copy .env.example .env
```

2. Ajuste `.env` para produção, usando Postgres como serviço persistente:

```bash
SECRET_KEY=sua-chave-secreta
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
ALLOWED_ORIGINS=https://seusite.com
ENVIRONMENT=production
```

3. No Render, crie um Web Service usando Docker e defina as variáveis de ambiente acima.

4. No Fly.io, configure as variáveis secretas:

```bash
fly secrets set SECRET_KEY="sua-chave-secreta" DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE" ALLOWED_ORIGINS="https://seusite.com" ENVIRONMENT="production"
```

5. O comando de startup já está preparado para usar `PORT` do ambiente:

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 cantina_api.main:app --bind 0.0.0.0:$PORT
```

6. Em produção, o esquema deve ser gerenciado via Alembic e não por `init_db()`.

## Segurança e considerações de produção

- Não deixe `SECRET_KEY` embutido em `app/core/security.py`. Em produção, exporte via variável de ambiente e carregue com `pydantic.BaseSettings` ou similar.
- Configure `DATABASE_URL` para apontar para um SGBD apropriado (Postgres, MySQL) e ajuste parâmetros de pool.
- Substitua `origins = ["*"]` no middleware CORS por domínios específicos quando for para produção.

## Boas práticas de desenvolvimento aplicadas

- Separação em camadas: `routers` (interface), `services` (regras), `models` (persistência), `schemas` (validação), `core` (infra). Isso facilita testes e manutenção.
- Injeção de dependências do FastAPI para facilitar substituição por doubles/mocks em testes.
- Testes automatizados integrados ao repositório para garantir regressões mínimas.

## Diretrizes para extensão e manutenção

- Para adicionar novo recurso (ex.: pedidos): crie `app/models/pedido.py`, `app/schemas/pedido.py`, `app/services/pedido_service.py`, e `app/api/v1/routers/pedidos.py`. Escreva testes unitários para service e testes de integração para endpoints.
- Mantenha a lógica de negócio nos `services`: routers apenas recebem entrada (schemas), chamam services e retornam resultados/erros HTTP apropriados.

## Comandos úteis

- Executar testes: `& ".venv/Scripts/python.exe" -m pytest -q`
- Rodar servidor local: `uvicorn cantina_api.main:app --reload`
- Criar migração: `alembic revision --autogenerate -m "mensagem"`

## Contribuição

Contribuições são bem-vindas. Para mudanças significativas abra uma issue descrevendo o objetivo. Use branches temáticos e inclua testes que cubram novas funcionalidades.

---

README atualizado para refletir a arquitetura e as correções aplicadas durante o desenvolvimento e verificação automática de testes.
