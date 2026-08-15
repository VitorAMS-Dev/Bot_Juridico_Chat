import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ..database import get_connection


def get(telefone: str) -> Optional[dict[str, Any]]:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT telefone, estado, dados_json, atualizado_em "
            "FROM conversation_sessions WHERE telefone = ?",
            (telefone,),
        ).fetchone()
    if row is None:
        return None
    return {
        "telefone": row["telefone"],
        "estado": row["estado"],
        "dados": json.loads(row["dados_json"]),
        "atualizado_em": row["atualizado_em"],
    }


def save(telefone: str, estado: str, dados: Dict[str, Any]) -> None:
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO conversation_sessions "
            "(telefone, estado, dados_json, atualizado_em) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(telefone) DO UPDATE SET estado = excluded.estado, "
            "dados_json = excluded.dados_json, atualizado_em = excluded.atualizado_em",
            (
                telefone,
                estado,
                json.dumps(dados, ensure_ascii=True),
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def delete(telefone: str) -> None:
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM conversation_sessions WHERE telefone = ?", (telefone,)
        )