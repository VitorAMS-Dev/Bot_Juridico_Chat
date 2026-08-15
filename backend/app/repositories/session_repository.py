import sqlite3
from datetime import datetime, timezone
from typing import Optional

from ..database import get_connection


def upsert(telefone: str, expira_em: str, estado: str) -> None:
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO admin_sessions (telefone, expira_em, estado) VALUES (?, ?, ?) "
            "ON CONFLICT(telefone) DO UPDATE SET expira_em = excluded.expira_em, "
            "estado = excluded.estado",
            (telefone, expira_em, estado),
        )


def find_by_phone(telefone: str) -> Optional[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            "SELECT id, telefone, expira_em, estado FROM admin_sessions "
            "WHERE telefone = ?",
            (telefone,),
        ).fetchone()


def update_state(telefone: str, estado: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE admin_sessions SET estado = ? WHERE telefone = ?",
            (estado, telefone),
        )
        return cursor.rowcount == 1


def delete(telefone: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM admin_sessions WHERE telefone = ?", (telefone,)
        )
        return cursor.rowcount == 1


def is_expired(expira_em: str) -> bool:
    expiration = datetime.fromisoformat(expira_em)
    return expiration <= datetime.now(timezone.utc)
