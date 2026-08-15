from app.repositories import session_repository


def test_admin_code_and_password_create_session(client):
    code_response = client.post(
        "/webhook",
        data={"From": "whatsapp:+5511777777777", "Body": "secret-test"},
    )
    assert code_response.status_code == 200
    assert b"Digite sua senha" in code_response.data

    password_response = client.post(
        "/webhook",
        data={"From": "whatsapp:+5511777777777", "Body": "password-test"},
    )
    assert b"Acesso administrativo autorizado" in password_response.data
    assert session_repository.find_by_phone("+5511777777777") is not None


def test_wrong_admin_password_does_not_create_session(client):
    client.post(
        "/webhook",
        data={"From": "whatsapp:+5511666666666", "Body": "secret-test"},
    )
    response = client.post(
        "/webhook",
        data={"From": "whatsapp:+5511666666666", "Body": "wrong-password"},
    )
    assert b"Senha incorreta" in response.data
    assert session_repository.find_by_phone("+5511666666666") is None
