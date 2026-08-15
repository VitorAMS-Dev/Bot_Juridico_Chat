import logging

from flask import Blueprint, Response, current_app, request
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from ..config import load_config
from ..services.conversation_service import handle_message

logger = logging.getLogger(__name__)

whatsapp_blueprint = Blueprint("whatsapp", __name__)


@whatsapp_blueprint.route("/webhook", methods=["POST"])
def webhook() -> Response:
    config = load_config()
    if config["VALIDATE_TWILIO_SIGNATURE"] and not _is_valid_twilio_request(config):
        return Response("Forbidden", status=403)

    phone = request.form.get("From", "").strip()
    message = request.form.get("Body", "")
    if not phone:
        return Response("Bad Request", status=400)

    response = MessagingResponse()
    try:
        response.message(handle_message(phone, message))
    except Exception:
        current_app.logger.exception("Falha técnica no processamento do webhook.")
        response.message(
            "Tivemos um problema ao processar sua solicitação. "
            "Tente novamente em alguns instantes."
        )
    return Response(str(response), mimetype="application/xml")


def _is_valid_twilio_request(config: dict) -> bool:
    url = str(config["TWILIO_WEBHOOK_URL"] or request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    validator = RequestValidator(str(config["TWILIO_AUTH_TOKEN"]))
    return validator.validate(url, request.form.to_dict(), signature)
