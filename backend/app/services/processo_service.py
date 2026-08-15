import sqlite3
from typing import Optional

from ..models.processo import Processo
from ..repositories import processo_repository
from ..utils.validators import is_non_empty_text, is_valid_process_number


class ProcessoValidationError(ValueError):
	"""Raised when process data does not satisfy the business rules."""


def normalize_process_number(numero: str) -> str:
	normalized = "".join(numero.split())
	if not is_valid_process_number(normalized):
		raise ProcessoValidationError("Número de processo inválido.")
	return normalized


def get_process(numero: str) -> Optional[Processo]:
	normalized = normalize_process_number(numero)
	row = processo_repository.find_by_number(normalized)
	return Processo.from_row(row) if row else None


def create_process(numero: str, status: str, observacao: str) -> Processo:
	normalized = normalize_process_number(numero)
	if not is_non_empty_text(status, max_length=120):
		raise ProcessoValidationError("Status inválido.")
	if not is_non_empty_text(observacao):
		raise ProcessoValidationError("Observação inválida.")

	try:
		processo_repository.create(normalized, status.strip(), observacao.strip())
	except sqlite3.IntegrityError as exc:
		raise ProcessoValidationError("Já existe um processo com esse número.") from exc

	process = get_process(normalized)
	if process is None:
		raise RuntimeError("Processo criado, mas não pôde ser recuperado.")
	return process


def update_process(numero: str, status: str, observacao: str) -> Processo:
	normalized = normalize_process_number(numero)
	if not is_non_empty_text(status, max_length=120):
		raise ProcessoValidationError("Status inválido.")
	if not is_non_empty_text(observacao):
		raise ProcessoValidationError("Observação inválida.")
	if not processo_repository.update(normalized, status.strip(), observacao.strip()):
		raise ProcessoValidationError("Processo não encontrado.")

	process = get_process(normalized)
	if process is None:
		raise RuntimeError("Processo atualizado, mas não pôde ser recuperado.")
	return process


def delete_process(numero: str) -> None:
	normalized = normalize_process_number(numero)
	if not processo_repository.delete(normalized):
		raise ProcessoValidationError("Processo não encontrado.")
