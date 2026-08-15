import re


def is_valid_process_number(number: str) -> bool:
    if not number:
        return False
    normalized = re.sub(r"\s+", "", number)
    return bool(re.fullmatch(r"\d{8,20}", normalized))


def is_valid_phone_number(phone: str) -> bool:
    if not phone:
        return False
    normalized = re.sub(r"[\s()+-]", "", phone)
    return bool(re.fullmatch(r"\d{10,15}", normalized))


def is_non_empty_text(text: str, max_length: int = 1000) -> bool:
    if not text:
        return False
    return bool(text.strip()) and len(text.strip()) <= max_length
