import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

REQUIRED_VARS = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN",
    "TWILIO_WHATSAPP_NUMBER",
    "DOUTORA_NUMERO",
    "ADMIN_SECRET_CODE",
    "ADMIN_PASSWORD",
]


def _get_env_value(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if isinstance(value, str):
        value = value.strip()
    return value


def load_config() -> Dict[str, str | int]:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    config = {
        "TWILIO_ACCOUNT_SID": _get_env_value("TWILIO_ACCOUNT_SID"),
        "TWILIO_AUTH_TOKEN": _get_env_value("TWILIO_AUTH_TOKEN"),
        "TWILIO_WHATSAPP_NUMBER": _get_env_value("TWILIO_WHATSAPP_NUMBER"),
        "DOUTORA_NUMERO": _get_env_value("DOUTORA_NUMERO"),
        "ADMIN_SECRET_CODE": _get_env_value("ADMIN_SECRET_CODE"),
        "ADMIN_PASSWORD": _get_env_value("ADMIN_PASSWORD"),
        "ADMIN_SESSION_MINUTES": _get_env_value("ADMIN_SESSION_MINUTES", "15"),
        "CONTACT_COOLDOWN_MINUTES": _get_env_value("CONTACT_COOLDOWN_MINUTES", "5"),
        "VALIDATE_TWILIO_SIGNATURE": _get_env_value("VALIDATE_TWILIO_SIGNATURE", "false"),
        "TWILIO_WEBHOOK_URL": _get_env_value("TWILIO_WEBHOOK_URL", ""),
        "DATABASE_PATH": _get_env_value("DATABASE_PATH", "processos.db"),
        "FLASK_ENV": _get_env_value("FLASK_ENV", "development"),
    }

    missing = [name for name in REQUIRED_VARS if not config.get(name)]
    if missing:
        raise RuntimeError(
            "Ambiente incompleto: defina as variáveis obrigatórias no arquivo .env ou no ambiente."
        )

    try:
        config["ADMIN_SESSION_MINUTES"] = int(config["ADMIN_SESSION_MINUTES"])
    except (TypeError, ValueError):
        raise RuntimeError("ADMIN_SESSION_MINUTES deve ser um número inteiro positivo.")

    if config["ADMIN_SESSION_MINUTES"] <= 0:
        raise RuntimeError("ADMIN_SESSION_MINUTES deve ser maior que zero.")

    try:
        config["CONTACT_COOLDOWN_MINUTES"] = int(config["CONTACT_COOLDOWN_MINUTES"])
    except (TypeError, ValueError):
        raise RuntimeError("CONTACT_COOLDOWN_MINUTES deve ser um número inteiro não negativo.")

    if config["CONTACT_COOLDOWN_MINUTES"] < 0:
        raise RuntimeError("CONTACT_COOLDOWN_MINUTES deve ser maior ou igual a zero.")

    config["VALIDATE_TWILIO_SIGNATURE"] = (
        str(config["VALIDATE_TWILIO_SIGNATURE"]).lower() == "true"
    )

    return config
