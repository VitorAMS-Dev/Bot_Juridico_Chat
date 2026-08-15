import sqlite3
from datetime import datetime, timezone
from typing import Optional

from ..database import get_connection


def _now() -> str:
	return datetime.now(timezone.utc).isoformat()


def create_pending(telefone: str) -> int:
	with get_connection() as connection:
		cursor = connection.execute(
			"INSERT INTO contatos (telefone, solicitado_em, atendido) "
			"VALUES (?, ?, 0)",
			(telefone, _now()),
		)
		return int(cursor.lastrowid)


def has_recent_pending(telefone: str, since: str) -> bool:
	with get_connection() as connection:
		result = connection.execute(
			"SELECT 1 FROM contatos "
			"WHERE telefone = ? AND atendido = 0 AND solicitado_em >= ? LIMIT 1",
			(telefone, since),
		).fetchone()
		return result is not None


def find_pending(telefone: str) -> Optional[sqlite3.Row]:
	with get_connection() as connection:
		return connection.execute(
			"SELECT id, telefone, solicitado_em, atendido FROM contatos "
			"WHERE telefone = ? AND atendido = 0 "
			"ORDER BY solicitado_em DESC LIMIT 1",
			(telefone,),
		).fetchone()


def mark_attended(contact_id: int) -> bool:
	with get_connection() as connection:
		cursor = connection.execute(
			"UPDATE contatos SET atendido = 1 WHERE id = ?", (contact_id,)
		)
		return cursor.rowcount == 1
