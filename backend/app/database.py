import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .config import load_config


def get_database_path() -> str:
    config = load_config()
    return config["DATABASE_PATH"]


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    path = Path(get_database_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    """Create the application schema without deleting existing data."""
    schema = """
    CREATE TABLE IF NOT EXISTS processos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL,
        observacao TEXT NOT NULL,
        atualizado_em TEXT NOT NULL,
        criado_em TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefone TEXT NOT NULL,
        solicitado_em TEXT NOT NULL,
        atendido INTEGER NOT NULL DEFAULT 0 CHECK (atendido IN (0, 1))
    );

    CREATE TABLE IF NOT EXISTS admin_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefone TEXT NOT NULL UNIQUE,
        expira_em TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'MAIN_MENU'
    );

    CREATE TABLE IF NOT EXISTS conversation_sessions (
        telefone TEXT PRIMARY KEY,
        estado TEXT NOT NULL,
        dados_json TEXT NOT NULL DEFAULT '{}',
        atualizado_em TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS message_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefone TEXT NOT NULL,
        mensagem TEXT NOT NULL,
        tipo TEXT NOT NULL,
        criado_em TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_contatos_telefone_data
        ON contatos (telefone, solicitado_em);
    CREATE INDEX IF NOT EXISTS idx_message_logs_telefone_data
        ON message_logs (telefone, criado_em);
    """

    with get_connection() as connection:
        connection.executescript(schema)
