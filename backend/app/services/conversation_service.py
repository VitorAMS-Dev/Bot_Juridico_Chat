import logging
from typing import Any, Dict

from ..repositories import conversation_repository
from ..utils.validators import is_non_empty_text, is_valid_process_number
from . import admin_service, processo_service
from .notificacao_service import NotificationError, notificar_doutora

logger = logging.getLogger(__name__)

MAIN_MENU = "MAIN_MENU"
WAITING_PROCESS_NUMBER = "WAITING_PROCESS_NUMBER"
WAITING_ADMIN_PASSWORD = "WAITING_ADMIN_PASSWORD"
ADMIN_MENU = "ADMIN_MENU"
ADMIN_CREATE_PROCESS_NUMBER = "ADMIN_CREATE_PROCESS_NUMBER"
ADMIN_CREATE_STATUS = "ADMIN_CREATE_STATUS"
ADMIN_CREATE_OBSERVATION = "ADMIN_CREATE_OBSERVATION"
ADMIN_CREATE_CONFIRMATION = "ADMIN_CREATE_CONFIRMATION"
ADMIN_UPDATE_PROCESS_NUMBER = "ADMIN_UPDATE_PROCESS_NUMBER"
ADMIN_UPDATE_STATUS = "ADMIN_UPDATE_STATUS"
ADMIN_UPDATE_OBSERVATION = "ADMIN_UPDATE_OBSERVATION"
ADMIN_UPDATE_CONFIRMATION = "ADMIN_UPDATE_CONFIRMATION"
ADMIN_DELETE_PROCESS_NUMBER = "ADMIN_DELETE_PROCESS_NUMBER"
ADMIN_DELETE_CONFIRMATION = "ADMIN_DELETE_CONFIRMATION"
ADMIN_READ_PROCESS_NUMBER = "ADMIN_READ_PROCESS_NUMBER"

MENU = (
    "Olá! Seja bem-vindo(a).\n\n"
    "Como posso ajudar?\n\n"
    "1 - Consultar andamento do meu processo\n"
    "2 - Falar com a doutora"
)
ADMIN_MENU_TEXT = (
    "Acesso administrativo autorizado.\n\n"
    "Escolha uma opção:\n\n"
    "1 - Criar processo\n2 - Atualizar processo\n3 - Deletar processo\n"
    "4 - Consultar processo\n0 - Sair"
)


def _phone(value: str) -> str:
    return value.removeprefix("whatsapp:").strip()


def _session(phone: str) -> tuple[str, Dict[str, Any]]:
    current = conversation_repository.get(phone)
    if current is None:
        return MAIN_MENU, {}
    return str(current["estado"]), dict(current["dados"])


def _save(phone: str, state: str, data: Dict[str, Any]) -> str:
    conversation_repository.save(phone, state, data)
    return state


def _admin_session(phone: str) -> bool:
    return admin_service.get_active_session(phone) is not None


def _number(text: str) -> str | None:
    normalized = "".join(text.split())
    return normalized if is_valid_process_number(normalized) else None


def handle_message(phone: str, message: str) -> str:
    """Process one inbound message and return the customer-facing response."""
    phone = _phone(phone)
    text = message.strip() if message else ""
    if not is_non_empty_text(text, max_length=2000):
        return "Não consegui identificar sua mensagem.\n\n" + MENU

    state, data = _session(phone)
    if admin_service.verify_secret_code(text) and not _admin_session(phone):
        _save(phone, WAITING_ADMIN_PASSWORD, {})
        return "Acesso administrativo.\n\nDigite sua senha:"

    if state == WAITING_ADMIN_PASSWORD:
        if admin_service.verify_admin_password(text):
            admin_service.create_session(phone)
            _save(phone, ADMIN_MENU, {})
            return ADMIN_MENU_TEXT
        _save(phone, MAIN_MENU, {})
        return "Senha incorreta. Acesso não autorizado.\n\n" + MENU

    if _admin_session(phone):
        return _handle_admin(phone, state, data, text)

    return _handle_client(phone, state, text)


def _handle_client(phone: str, state: str, text: str) -> str:
    if state == WAITING_PROCESS_NUMBER:
        number = _number(text)
        if number is None:
            return "Informe um número de processo válido, somente com os dígitos."
        process = processo_service.get_process(number)
        if process is None:
            _save(phone, MAIN_MENU, {})
            return "Processo não encontrado.\n\n" + MENU
        _save(phone, MAIN_MENU, {})
        return (
            f"Processo: {process.numero}\n\nStatus: {process.status}\n\n"
            f"Observação: {process.observacao}\n\n"
            f"Última atualização: {process.atualizado_em.strftime('%d/%m/%Y %H:%M')}\n\n"
            "1 - Consultar outro processo\n2 - Falar com a doutora\n0 - Menu principal"
        )

    if text == "1":
        _save(phone, WAITING_PROCESS_NUMBER, {})
        return "Claro! Para consultar seu processo, informe o número completo do processo."
    if text == "2":
        try:
            requested = notificar_doutora(phone)
        except (NotificationError, ValueError):
            logger.exception("Falha ao registrar solicitação de contato.")
            return "Tivemos um problema ao registrar sua solicitação. Tente novamente em instantes."
        _save(phone, MAIN_MENU, {})
        if not requested:
            return "Sua solicitação já está registrada. A doutora entrará em contato assim que possível."
        return "Solicitação registrada!\n\nJá avisei a doutora. Assim que possível, ela entrará em contato."
    if text == "0":
        _save(phone, MAIN_MENU, {})
        return MENU
    _save(phone, MAIN_MENU, {})
    return MENU


def _handle_admin(phone: str, state: str, data: Dict[str, Any], text: str) -> str:
    if state in (ADMIN_MENU, MAIN_MENU):
        if text == "0":
            admin_service.logout(phone)
            conversation_repository.delete(phone)
            return "Sessão administrativa encerrada com segurança.\n\n" + MENU
        transitions = {
            "1": (ADMIN_CREATE_PROCESS_NUMBER, "Informe o número do processo:"),
            "2": (ADMIN_UPDATE_PROCESS_NUMBER, "Informe o número do processo que deseja atualizar:"),
            "3": (ADMIN_DELETE_PROCESS_NUMBER, "Informe o número do processo que deseja deletar:"),
            "4": (ADMIN_READ_PROCESS_NUMBER, "Informe o número do processo que deseja consultar:"),
        }
        next_state, response = transitions.get(text, (ADMIN_MENU, ADMIN_MENU_TEXT))
        _save(phone, next_state, {})
        return response

    number = _number(text)
    if state in (ADMIN_CREATE_PROCESS_NUMBER, ADMIN_UPDATE_PROCESS_NUMBER,
                 ADMIN_DELETE_PROCESS_NUMBER, ADMIN_READ_PROCESS_NUMBER):
        if number is None:
            return "Informe um número de processo válido, somente com os dígitos."
        process = processo_service.get_process(number)
        if state == ADMIN_CREATE_PROCESS_NUMBER:
            _save(phone, ADMIN_CREATE_STATUS, {"numero": number})
            return "Informe o status do processo:"
        if process is None:
            _save(phone, ADMIN_MENU, {})
            return "Processo não encontrado.\n\n" + ADMIN_MENU_TEXT
        if state == ADMIN_UPDATE_PROCESS_NUMBER:
            _save(phone, ADMIN_UPDATE_STATUS, {"numero": number})
            return f"Dados atuais:\nStatus: {process.status}\nObservação: {process.observacao}\n\nQual será o novo status?"
        if state == ADMIN_DELETE_PROCESS_NUMBER:
            _save(phone, ADMIN_DELETE_CONFIRMATION, {"numero": number})
            return f"Atenção: você está prestes a excluir:\n\nProcesso: {process.numero}\nStatus: {process.status}\n\n1 - Confirmar exclusão\n2 - Cancelar"
        _save(phone, ADMIN_MENU, {})
        return f"Processo: {process.numero}\nStatus: {process.status}\nObservação: {process.observacao}\nCriado em: {process.criado_em}\nÚltima atualização: {process.atualizado_em}"

    if state == ADMIN_CREATE_STATUS:
        if not is_non_empty_text(text, 120):
            return "Informe um status válido."
        data["status"] = text
        _save(phone, ADMIN_CREATE_OBSERVATION, data)
        return "Informe uma observação para este processo:"
    if state == ADMIN_CREATE_OBSERVATION:
        if not is_non_empty_text(text):
            return "Informe uma observação válida."
        data["observacao"] = text
        _save(phone, ADMIN_CREATE_CONFIRMATION, data)
        return f"Confira os dados:\n\nProcesso: {data['numero']}\nStatus: {data['status']}\nObservação: {text}\n\n1 - Confirmar\n2 - Corrigir\n0 - Cancelar"
    if state == ADMIN_CREATE_CONFIRMATION:
        if text == "1":
            try:
                processo_service.create_process(data["numero"], data["status"], data["observacao"])
            except ValueError as exc:
                _save(phone, ADMIN_MENU, {})
                return f"Não foi possível criar o processo: {exc}"
            _save(phone, ADMIN_MENU, {})
            return "Processo criado com sucesso.\n\n" + ADMIN_MENU_TEXT
        if text == "2":
            _save(phone, ADMIN_CREATE_STATUS, {"numero": data["numero"]})
            return "Informe o status do processo:"
        _save(phone, ADMIN_MENU, {})
        return ADMIN_MENU_TEXT
    if state == ADMIN_UPDATE_STATUS:
        if not is_non_empty_text(text, 120):
            return "Informe um status válido."
        data["status"] = text
        _save(phone, ADMIN_UPDATE_OBSERVATION, data)
        return "Informe a nova observação:"
    if state == ADMIN_UPDATE_OBSERVATION:
        if not is_non_empty_text(text):
            return "Informe uma observação válida."
        data["observacao"] = text
        _save(phone, ADMIN_UPDATE_CONFIRMATION, data)
        return f"Confirme a atualização:\n\nProcesso: {data['numero']}\nStatus: {data['status']}\nObservação: {text}\n\n1 - Confirmar\n2 - Corrigir\n0 - Cancelar"
    if state == ADMIN_UPDATE_CONFIRMATION:
        if text == "1":
            try:
                processo_service.update_process(data["numero"], data["status"], data["observacao"])
            except ValueError as exc:
                _save(phone, ADMIN_MENU, {})
                return f"Não foi possível atualizar o processo: {exc}"
            _save(phone, ADMIN_MENU, {})
            return "Processo atualizado com sucesso.\n\n" + ADMIN_MENU_TEXT
        if text == "2":
            _save(phone, ADMIN_UPDATE_STATUS, {"numero": data["numero"]})
            return "Qual será o novo status?"
        _save(phone, ADMIN_MENU, {})
        return ADMIN_MENU_TEXT
    if state == ADMIN_DELETE_CONFIRMATION:
        if text == "1":
            processo_service.delete_process(data["numero"])
            _save(phone, ADMIN_MENU, {})
            return "Processo excluído com sucesso.\n\n" + ADMIN_MENU_TEXT
        _save(phone, ADMIN_MENU, {})
        return ADMIN_MENU_TEXT

    _save(phone, ADMIN_MENU, {})
    return ADMIN_MENU_TEXT