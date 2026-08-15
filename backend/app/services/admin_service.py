import hmac
from datetime import datetime, timedelta, timezone

from ..config import load_config
from ..repositories import session_repository
from ..utils.security import hash_password, verify_password


MAIN_MENU_STATE = "MAIN_MENU"


def verify_secret_code(code: str) -> bool:
	configured_code = str(load_config()["ADMIN_SECRET_CODE"])
	return hmac.compare_digest(code.strip(), configured_code)


def verify_admin_password(password: str) -> bool:
	configured_password = str(load_config()["ADMIN_PASSWORD"])
	configured_hash = hash_password(configured_password)
	return verify_password(password, configured_hash)


def create_session(telefone: str, estado: str = MAIN_MENU_STATE) -> None:
	minutes = int(load_config()["ADMIN_SESSION_MINUTES"])
	expiration = datetime.now(timezone.utc) + timedelta(minutes=minutes)
	session_repository.upsert(telefone, expiration.isoformat(), estado)


def get_active_session(telefone: str):
	session = session_repository.find_by_phone(telefone)
	if session is None:
		return None
	if session_repository.is_expired(session["expira_em"]):
		session_repository.delete(telefone)
		return None
	return session


def update_state(telefone: str, estado: str) -> bool:
	if get_active_session(telefone) is None:
		return False
	return session_repository.update_state(telefone, estado)


def logout(telefone: str) -> None:
	session_repository.delete(telefone)
