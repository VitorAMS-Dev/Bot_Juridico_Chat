import logging
from datetime import datetime, timedelta, timezone

from ..config import load_config
from ..repositories import contato_repository
from ..utils.validators import is_valid_phone_number
from .whatsapp_service import send_message

logger = logging.getLogger(__name__)


class NotificationError(RuntimeError):
	"""Raised when a doctor notification cannot be delivered."""


def _utc_now() -> datetime:
	return datetime.now(timezone.utc)


def notificar_doutora(telefone_cliente: str) -> bool:
	"""Register a contact request and notify the doctor once per cooldown."""
	if not is_valid_phone_number(telefone_cliente):
		raise ValueError("Telefone inválido.")

	config = load_config()
	cooldown = int(config.get("CONTACT_COOLDOWN_MINUTES", 5))
	since = (_utc_now() - timedelta(minutes=cooldown)).isoformat()
	if contato_repository.has_recent_pending(telefone_cliente, since):
		return False

	contact_id = contato_repository.create_pending(telefone_cliente)
	notification = (
		"🔔 NOVA SOLICITAÇÃO DE CONTATO\n\n"
		"Um cliente solicitou falar diretamente com você.\n\n"
		f"📱 Telefone: {telefone_cliente}\n"
		f"🕒 Data: {_utc_now().strftime('%d/%m/%Y %H:%M')}\n\n"
		"📌 Origem: WhatsApp"
	)

	try:
		send_message(str(config["DOUTORA_NUMERO"]), notification)
	except Exception as exc:
		logger.exception("Falha técnica ao enviar notificação de contato.")
		raise NotificationError("Não foi possível enviar a notificação.") from exc

	if contact_id <= 0:
		raise NotificationError("Solicitação de contato inválida.")
	return True
