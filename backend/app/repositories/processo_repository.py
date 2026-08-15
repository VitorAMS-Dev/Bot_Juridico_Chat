import sqlite3
from datetime import datetime, timezone
from typing import Optional

from ..database import get_connection


def _now() -> str:
	return datetime.now(timezone.utc).isoformat()


def find_by_number(numero: str) -> Optional[sqlite3.Row]:
	with get_connection() as connection:
		return connection.execute(
			"SELECT id, numero, status, observacao, atualizado_em, criado_em "
			"FROM processos WHERE numero = ?",
			(numero,),
		).fetchone()


def create(numero: str, status: str, observacao: str) -> int:
	timestamp = _now()
	with get_connection() as connection:
		cursor = connection.execute(
			"INSERT INTO processos "
			"(numero, status, observacao, atualizado_em, criado_em) "
			"VALUES (?, ?, ?, ?, ?)",
			(numero, status, observacao, timestamp, timestamp),
		)
		return int(cursor.lastrowid)


def update(numero: str, status: str, observacao: str) -> bool:
	with get_connection() as connection:
		cursor = connection.execute(
			"UPDATE processos SET status = ?, observacao = ?, atualizado_em = ? "
			"WHERE numero = ?",
			(status, observacao, _now(), numero),
		)
		return cursor.rowcount == 1


def delete(numero: str) -> bool:
	with get_connection() as connection:
		cursor = connection.execute(
			"DELETE FROM processos WHERE numero = ?", (numero,)
		)
		return cursor.rowcount == 1
