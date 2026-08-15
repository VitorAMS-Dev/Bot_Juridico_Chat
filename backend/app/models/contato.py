from dataclasses import dataclass
from datetime import datetime
import sqlite3


@dataclass
class Contato:
    id: int
    telefone: str
    solicitado_em: datetime
    atendido: bool

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Contato":
        return cls(
            id=int(row["id"]),
            telefone=str(row["telefone"]),
            solicitado_em=datetime.fromisoformat(row["solicitado_em"]),
            atendido=bool(row["atendido"]),
        )
