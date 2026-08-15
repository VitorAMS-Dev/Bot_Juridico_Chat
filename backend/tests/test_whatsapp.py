def test_initial_menu_and_process_state(client):
    first = client.post(
        "/webhook",
        data={"From": "whatsapp:+5511999999999", "Body": "oi"},
    )
    assert first.status_code == 200
    assert b"Consultar andamento" in first.data

    second = client.post(
        "/webhook",
        data={"From": "whatsapp:+5511999999999", "Body": "1"},
    )
    assert second.status_code == 200
    assert b"processo" in second.data


def test_unknown_message_returns_menu(client):
    response = client.post(
        "/webhook",
        data={"From": "whatsapp:+5511888888888", "Body": "mensagem inesperada"},
    )
    assert response.status_code == 200
    assert b"Falar com a doutora" in response.data
