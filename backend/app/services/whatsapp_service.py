from typing import Any

from ..config import load_config


def _format_whatsapp_number(number: str) -> str:
    return number if number.startswith("whatsapp:") else f"whatsapp:{number}"


def _get_client() -> Any:
    from twilio.rest import Client

    config = load_config()
    return Client(config["TWILIO_ACCOUNT_SID"], config["TWILIO_AUTH_TOKEN"])


def send_message(to_number: str, body: str) -> str:
    """Send a WhatsApp message through Twilio and return its message SID."""
    if not body.strip():
        raise ValueError("A mensagem não pode estar vazia.")
    config = load_config()
    message = _get_client().messages.create(
        body=body,
        from_=_format_whatsapp_number(str(config["TWILIO_WHATSAPP_NUMBER"])),
        to=_format_whatsapp_number(to_number),
    )
    return str(message.sid)
def send_message(to_number: str, body: str) -> None:
    raise NotImplementedError("Twilio integration not implemented yet")
