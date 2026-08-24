# Bot Jurídico de WhatsApp

Sistema automatizado backend para um escritório de advocacia, integrado ao WhatsApp através da Twilio API. Permite que clientes consultem o andamento de seus processos judiciais e solicitem contato direto com a doutora.

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Execução](#execução)
- [Testes](#testes)
- [Uso](#uso)
- [Integração com Twilio](#integração-com-twilio)
- [Segurança e LGPD](#segurança-e-lgpd)
- [Deploy](#deploy)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O **Bot Jurídico de WhatsApp** automatiza a comunicação entre clientes e um escritório de advocacia através do WhatsApp. O sistema oferece:

- **Consulta de processos**: clientes consultam o andamento de seus casos digitando o número do processo.
- **Contato direto**: clientes podem solicitar falar com a doutora através de um botão no WhatsApp.
- **Painel administrativo**: a doutora pode criar, atualizar e deletar processos via WhatsApp.
- **Sessões administrativas**: acesso seguro com código secreto e senha, com expiração automática.
- **Notificações**: a doutora recebe notificações instantâneas quando um cliente solicita contato.
- **Conformidade LGPD**: design focado em privacidade de dados e segurança jurídica.

## 🛠 Tecnologias

- **Backend**: Python 3.14+
- **Framework Web**: Flask 3.1+
- **Banco de Dados**: SQLite 3
- **Integração WhatsApp**: Twilio API 9.10+
- **Segurança**: Werkzeug (password hashing adaptativo)
- **Testes**: pytest 9.1+
- **Gerenciamento de Ambiente**: python-dotenv 1.2+

## 🏗 Arquitetura

```
Cliente WhatsApp
       ↓
   Twilio API
       ↓
  Webhook Flask
       ↓
  Conversation Service (Máquina de Estados)
       ↓
 Services (Processo, Admin, Notificação)
       ↓
 Repositories (Acesso ao Banco)
       ↓
  SQLite Database
```

### Fluxo de Notificação

```
Cliente solicita contato
       ↓
Webhook registra solicitação no banco
       ↓
Notification Service valida e respeita cooldown
       ↓
Twilio API envia mensagem para a doutora
       ↓
Doutora recebe notificação no WhatsApp
```

## 📂 Estrutura do Projeto

```
botJuridicoChat/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Factory Flask
│   │   ├── config.py                # Carregamento de .env e validação
│   │   ├── database.py              # Schema SQLite e conexão
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── whatsapp.py          # Webhook POST /webhook
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── conversation_service.py   # Máquina de estados
│   │   │   ├── processo_service.py       # Lógica de processos
│   │   │   ├── admin_service.py          # Autenticação e sessão
│   │   │   ├── notificacao_service.py    # Notificação doutora
│   │   │   └── whatsapp_service.py       # Cliente Twilio
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── processo_repository.py     # CRUD processos
│   │   │   ├── contato_repository.py      # Solicitações de contato
│   │   │   ├── session_repository.py      # Sessões administrativas
│   │   │   ├── conversation_repository.py # Estados conversas
│   │   │   └── message_log_repository.py  # Auditoria de mensagens
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── processo.py      # Dataclass Processo
│   │   │   └── contato.py       # Dataclass Contato
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py    # Validação de entrada
│   │       └── security.py      # Hashing de senha
│   │
│   ├── tests/
│   │   ├── conftest.py          # Fixtures pytest
│   │   ├── test_processos.py    # Testes CRUD
│   │   ├── test_whatsapp.py     # Testes webhook e fluxo
│   │   └── test_admin.py        # Testes autenticação
│   │
│   ├── run.py                   # Entry point
│   ├── requirements.txt          # Dependências
│   ├── README.md                # Documentação (este arquivo)
│   └── .gitignore               # Git ignore
│
├── .env                         # Variáveis de ambiente (desenvolvimento)
├── .env.example                 # Template de variáveis
├── .gitignore                   # Git ignore (raiz)
└── README.md                    # Este arquivo
```

## 🚀 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/botJuridicoChat.git
cd botJuridicoChat
```

### 2. Criar e ativar ambiente virtual

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores:

```bash
cp .env.example .env
```

Edite `.env` com seus valores:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+551140000000
DOUTORA_NUMERO=+5511999999999
ADMIN_SECRET_CODE=123456
ADMIN_PASSWORD=sua_senha_segura_aqui
ADMIN_SESSION_MINUTES=15
CONTACT_COOLDOWN_MINUTES=5
VALIDATE_TWILIO_SIGNATURE=false
TWILIO_WEBHOOK_URL=
DATABASE_PATH=processos.db
FLASK_ENV=development
```

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório | Padrão |
|----------|-----------|-------------|--------|
| `TWILIO_ACCOUNT_SID` | SID da conta Twilio | ✅ | - |
| `TWILIO_AUTH_TOKEN` | Token de autenticação Twilio | ✅ | - |
| `TWILIO_WHATSAPP_NUMBER` | Número WhatsApp Twilio | ✅ | - |
| `DOUTORA_NUMERO` | Telefone da doutora para notificações | ✅ | - |
| `ADMIN_SECRET_CODE` | Código secreto para acesso administrativo | ✅ | - |
| `ADMIN_PASSWORD` | Senha do administrador | ✅ | - |
| `ADMIN_SESSION_MINUTES` | Duração da sessão administrativo (minutos) | ❌ | 15 |
| `CONTACT_COOLDOWN_MINUTES` | Intervalo mínimo entre solicitações de contato (minutos) | ❌ | 5 |
| `VALIDATE_TWILIO_SIGNATURE` | Habilitar validação de assinatura Twilio | ❌ | false |
| `TWILIO_WEBHOOK_URL` | URL do webhook (necessária se validação habilitada) | ❌ | - |
| `DATABASE_PATH` | Caminho do banco SQLite | ❌ | processos.db |
| `FLASK_ENV` | Ambiente Flask (development/production) | ❌ | development |

### Configuração Twilio

#### 1. Criar conta Twilio

1. Acesse [twilio.com](https://www.twilio.com)
2. Crie uma conta
3. Acesse o Console
4. Copie `Account SID` e `Auth Token`

#### 2. Ativar WhatsApp Sandbox

1. No Console, vá para `Messaging` → `Channels` → `WhatsApp`
2. Configure o WhatsApp Sandbox
3. Copie o número `whatsapp:+1XXXXXXXXXX`

#### 3. Configurar Webhook

1. No Console, vá para `Messaging` → `Services` → seu serviço WhatsApp
2. Em `Inbound Settings`, configure:
   - **Webhook URL**: `https://seu-dominio.com/webhook`
   - **Method**: `POST`

#### 4. Ambiente de Desenvolvimento com ngrok

Para testar localmente, use [ngrok](https://ngrok.com):

```bash
ngrok http 5000
```

Isso retornará uma URL como `https://abc123.ngrok.io`. Configure esta URL como webhook no Twilio:

```bash
https://abc123.ngrok.io/webhook
```

## 🏃 Execução

### Modo Desenvolvimento

```bash
cd backend
python run.py
```

O servidor iniciará em `http://localhost:5000`.

### Com Variáveis de Ambiente Personalizadas

```powershell
$env:FLASK_ENV='development'
python run.py
```

### Com Validação Twilio Ativada (Produção)

```bash
export VALIDATE_TWILIO_SIGNATURE=true
export TWILIO_WEBHOOK_URL=https://seu-dominio.com/webhook
python run.py
```

## 🧪 Testes

### Rodar toda suíte de testes

```bash
cd backend
pytest
```

### Rodar com cobertura

```bash
pytest --cov=app --cov-report=html
```

### Rodar apenas uma categoria

```bash
pytest tests/test_processos.py      # Testes CRUD
pytest tests/test_whatsapp.py       # Testes webhook
pytest tests/test_admin.py          # Testes autenticação
```

### Testes inclusos

- ✅ CRUD de processos
- ✅ Validação de número de processo
- ✅ Menu inicial
- ✅ Máquina de estados cliente
- ✅ Mensagens desconhecidas
- ✅ Código administrativo
- ✅ Senha correta e incorreta

## 💬 Uso

### Fluxo Cliente

```
Cliente → "Oi"
Bot      ← "Olá! Seja bem-vindo(a)."
         ← "Como posso ajudar?"
         ← "1 - Consultar andamento do meu processo"
         ← "2 - Falar com a doutora"

Cliente → "1"
Bot      ← "Informe o número completo do processo."

Cliente → "12345678901234"
Bot      ← "Processo: 12345678901234"
         ← "Status: Em andamento"
         ← "Observação: Aguardando decisão do juiz"
         ← "Última atualização: 14/08/2026 10:30"

Cliente → "2"
Bot      ← "Solicitação registrada!"
         ← "Já avisei a doutora. Assim que possível, ela entrará em contato."

Doutora → (recebe notificação no WhatsApp)
```

### Fluxo Administrativo

```
Admin → "123456" (código secreto)
Bot   ← "Acesso administrativo. Digite sua senha:"

Admin → "senha_segura"
Bot   ← "Acesso administrativo autorizado."
      ← "Escolha uma opção:"
      ← "1 - Criar processo"
      ← "2 - Atualizar processo"
      ← "3 - Deletar processo"
      ← "4 - Consultar processo"
      ← "0 - Sair"

Admin → "1"
Bot   ← "Informe o número do processo:"

Admin → "98765432109876"
Bot   ← "Informe o status do processo:"

Admin → "Em andamento"
Bot   ← "Informe uma observação para este processo:"

Admin → "Entrada de pedido de habeas corpus"
Bot   ← "Confira os dados:"
      ← "Processo: 98765432109876"
      ← "Status: Em andamento"
      ← "Observação: Entrada de pedido de habeas corpus"
      ← "1 - Confirmar"
      ← "2 - Corrigir"
      ← "0 - Cancelar"

Admin → "1"
Bot   ← "Processo criado com sucesso."

Admin → "0"
Bot   ← "Sessão administrativa encerrada com segurança."
      ← "Olá! Seja bem-vindo(a)..."
```

## 🔐 Segurança e LGPD

### Protocolos de Segurança

- ✅ **SQL Injection**: Todas as queries usam parâmetros preparados (`?`)
- ✅ **Hashing de Senha**: Werkzeug adaptive hashing (pbkdf2:sha256)
- ✅ **Comparação Segura**: `hmac.compare_digest()` para código secreto
- ✅ **Validação de Entrada**: Números, telefones, textos limitados
- ✅ **Timeout de Sessão**: Sessão administrativo expira automaticamente
- ✅ **Logs Seguros**: Sem exposição de tokens ou senhas
- ✅ **Erro Genérico**: Falhas internas retornam mensagem neutra ao usuário

### Validação de Webhook Twilio

Em **produção**, sempre ative:

```env
VALIDATE_TWILIO_SIGNATURE=true
TWILIO_WEBHOOK_URL=https://seu-dominio.com/webhook
```

Isso previne que endpoints falsos enviem mensagens para o bot.

### Proteção contra Brute Force

⚠️ **Atual**: Não há limite de tentativas no código + password.

**Recomendações**:
1. Implementar contagem de tentativas falhadas
2. Adicionar bloqueio temporário (ex: 15 minutos após 3 falhas)
3. Registrar tentativas suspeitas em log de auditoria
4. Usar CAPTCHA ou verificação de segundo fator

### Privacidade e Conformidade

#### Dados Armazenados

1. **Tabela `processos`**
   - Número, status, observação, timestamps
   - Dados jurídicos sensíveis

2. **Tabela `contatos`**
   - Telefone do cliente, timestamp, atendido
   - Solicitações de contato

3. **Tabela `admin_sessions`**
   - Telefone administrativo, expiração, estado
   - Sessões ativas

4. **Tabela `conversation_sessions`**
   - Telefone, estado da conversa, dados JSON
   - Fluxo de conversa atual

5. **Tabela `message_logs`**
   - Telefone, mensagem, tipo, timestamp
   - Auditoria de mensagens

#### Finalidade dos Dados

- Permitir consulta de processo pelo cliente
- Notificar doutora de solicitação de contato
- Manter histórico administrativo seguro
- Rastrear estado da conversa

#### Retenção de Dados

**Recomendado**:
- `processos`: 5 anos (conforme legislação civil/processual)
- `contatos`: 2 anos
- `message_logs`: 1 ano
- `admin_sessions`: 24 horas (após expiração)
- `conversation_sessions`: 30 dias (após inatividade)

#### Direito de Exclusão (LGPD Art. 16)

Implementar script de limpeza:

```sql
-- Deletar conversa e logs de um cliente
DELETE FROM conversation_sessions WHERE telefone = '+55119999999999';
DELETE FROM message_logs WHERE telefone = '+55119999999999';
DELETE FROM contatos WHERE telefone = '+55119999999999';
```

#### Segurança do Banco SQLite

O arquivo `.db` contém dados sensíveis. Proteja com:

```bash
chmod 600 processos.db      # Linux/macOS
icacls processos.db /grant:r "%USERNAME%":(F) /inheritance:r  # Windows
```

### Proteção do `.env`

Nunca versione o `.env`. Ele deve estar no `.gitignore`:

```gitignore
.env
```

Compartilhe `.env.example` como template, sem valores reais.

## 🚀 Deploy

### Preparação

1. Ativar validação Twilio:
   ```env
   VALIDATE_TWILIO_SIGNATURE=true
   TWILIO_WEBHOOK_URL=https://seu-dominio-producao.com/webhook
   ```

2. Usar senha complexa:
   ```env
   ADMIN_PASSWORD=Abc@123DefGhiJkl$MnoPqrst2024
   ```

3. Usar código secreto aleatório:
   ```env
   ADMIN_SECRET_CODE=7293849572
   ```

4. Proteger banco:
   ```bash
   chmod 600 processos.db
   ```

### Opção 1: Heroku

```bash
cd backend
heroku login
heroku create seu-bot-juridico
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxxxx
heroku config:set TWILIO_AUTH_TOKEN=xxxxxx
# ... defina todas as variáveis
git push heroku main
```

### Opção 2: Railway

1. Conecte seu repositório em [railway.app](https://railway.app)
2. Configure variáveis de ambiente no dashboard
3. Deploy automático em cada push

### Opção 3: Docker

```dockerfile
FROM python:3.14-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 5000
CMD ["python", "run.py"]
```

```bash
docker build -t bot-juridico .
docker run -p 5000:5000 -e TWILIO_ACCOUNT_SID=AC... bot-juridico
```

### Opção 4: VPS/Servidor próprio

1. Install Python 3.14+
2. Clone repositório
3. Setup `.env`
4. Use `gunicorn` como production server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

5. Configure reverse proxy (nginx):

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. Use HTTPS com Let's Encrypt:

```bash
certbot certonly --nginx -d seu-dominio.com
```

## 📊 Banco de Dados

### Schema

```sql
-- Processos jurídicos
CREATE TABLE processos (
    id INTEGER PRIMARY KEY,
    numero TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    observacao TEXT NOT NULL,
    atualizado_em TEXT NOT NULL,
    criado_em TEXT NOT NULL
);

-- Solicitações de contato
CREATE TABLE contatos (
    id INTEGER PRIMARY KEY,
    telefone TEXT NOT NULL,
    solicitado_em TEXT NOT NULL,
    atendido INTEGER DEFAULT 0 CHECK (atendido IN (0, 1))
);

-- Sessões administrativas
CREATE TABLE admin_sessions (
    id INTEGER PRIMARY KEY,
    telefone TEXT NOT NULL UNIQUE,
    expira_em TEXT NOT NULL,
    estado TEXT DEFAULT 'MAIN_MENU'
);

-- Estados de conversa
CREATE TABLE conversation_sessions (
    telefone TEXT PRIMARY KEY,
    estado TEXT NOT NULL,
    dados_json TEXT DEFAULT '{}',
    atualizado_em TEXT NOT NULL
);

-- Logs de mensagens (auditoria)
CREATE TABLE message_logs (
    id INTEGER PRIMARY KEY,
    telefone TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    tipo TEXT NOT NULL,
    criado_em TEXT NOT NULL
);
```

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

Ative o ambiente virtual e instale dependências:

```bash
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

### "Ambiente incompleto: defina as variáveis obrigatórias"

Verifique se `.env` contém todas as variáveis obrigatórias:

```bash
cat .env
```

Copie de `.env.example` se necessário:

```bash
cp .env.example .env
```

### "sqlite3.OperationalError: no such table"

O banco não foi inicializado. Execute uma vez com validação:

```python
from app.database import initialize_database
initialize_database()
```

Ou simplesmente execute `python run.py` que inicializará automaticamente.

### Webhook recebe 403 Forbidden

Se `VALIDATE_TWILIO_SIGNATURE=true`, verifique:

1. `TWILIO_AUTH_TOKEN` está correto?
2. `TWILIO_WEBHOOK_URL` está correto?
3. ngrok URL é a mesma no Twilio?

Para debug, desative temporariamente:

```env
VALIDATE_TWILIO_SIGNATURE=false
```

### Sessão administrativa expira muito rápido

Aumente `ADMIN_SESSION_MINUTES`:

```env
ADMIN_SESSION_MINUTES=60
```

### Testes falhando

Certifique-se que está no diretório `backend`:

```bash
cd backend
pytest
```

## 📝 Licença

Este projeto é confidencial. Não é permitida distribuição sem autorização.

## 👨‍💼 Suporte

Para dúvidas ou problemas, entre em contato com o time de desenvolvimento.

---

**Versão**: 1.0.0  
**Última atualização**: 14 de agosto de 2026
