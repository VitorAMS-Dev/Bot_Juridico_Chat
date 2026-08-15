from dataclasses import dataclass
from datetime import datetime
import sqlite3


@dataclass
class Processo:
    id: int
    numero: str
    status: str
    observacao: str
    atualizado_em: datetime
    criado_em: datetime

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Processo":
        return cls(
            id=int(row["id"]),
            numero=str(row["numero"]),
            status=str(row["status"]),
            observacao=str(row["observacao"]),
            atualizado_em=datetime.fromisoformat(row["atualizado_em"]),
            criado_em=datetime.fromisoformat(row["criado_em"]),
        )
