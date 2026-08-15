from datetime import datetime, timezone

from ..database import get_connection


def create(telefone: str, mensagem: str, tipo: str) -> int:
    """Store only the minimum message metadata needed for auditing."""
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO message_logs (telefone, mensagem, tipo, criado_em) "
            "VALUES (?, ?, ?, ?)",
            (telefone, mensagem, tipo, datetime.now(timezone.utc).isoformat()),
        )
        return int(cursor.lastrowid)
