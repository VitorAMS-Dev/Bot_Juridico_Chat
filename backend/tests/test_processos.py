from app.services import processo_service


def test_create_find_update_and_delete_process():
    created = processo_service.create_process(
        "12345678901234", "Em andamento", "Aguardando atualização."
    )

    assert created.numero == "12345678901234"
    assert processo_service.get_process("12345678901234").status == "Em andamento"

    updated = processo_service.update_process(
        "12345678901234", "Encerrado", "Processo finalizado."
    )
    assert updated.status == "Encerrado"

    processo_service.delete_process("12345678901234")
    assert processo_service.get_process("12345678901234") is None


def test_invalid_process_number_is_rejected():
    try:
        processo_service.get_process("abc")
    except processo_service.ProcessoValidationError:
        pass
    else:
        raise AssertionError("Número inválido deveria ser rejeitado")
