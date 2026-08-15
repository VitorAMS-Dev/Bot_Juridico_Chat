# Bot Jurídico de WhatsApp

Projeto backend em Python e Flask para criação de um bot de WhatsApp que permite clientes consultarem processos e solicitar contato direto com a doutora.

## Tecnologias

- Python
- Flask
- SQLite
- Twilio API
- python-dotenv
- pytest

## Estrutura

- `app/`: código principal do backend
- `app/config.py`: configuração da aplicação e variáveis de ambiente
- `app/database.py`: conexão com SQLite
- `app/routes/whatsapp.py`: webhook do WhatsApp
- `app/services/`: lógica de negócio e integrações
- `app/repositories/`: acesso ao banco de dados
- `app/models/`: definições de entidades
- `app/utils/`: validações e segurança
- `tests/`: testes automatizados
- `run.py`: ponto de entrada para executar o servidor

## Instalação

1. Crie um ambiente virtual:

```bash
python -m venv .venv
```

1. Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

1. Instale dependências:

```bash
pip install -r requirements.txt
```

1. Copie o `.env.example` para `.env` e preencha as variáveis.

## Executar

```bash
python run.py
```

## Testar

```bash
pytest
```
