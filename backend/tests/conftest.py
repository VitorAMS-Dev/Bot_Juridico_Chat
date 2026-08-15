import pytest


@pytest.fixture(autouse=True)
def test_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "AC_test")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "test-token")
    monkeypatch.setenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+10000000000")
    monkeypatch.setenv("DOUTORA_NUMERO", "+5511000000000")
    monkeypatch.setenv("ADMIN_SECRET_CODE", "secret-test")
    monkeypatch.setenv("ADMIN_PASSWORD", "password-test")
    monkeypatch.setenv("ADMIN_SESSION_MINUTES", "15")
    monkeypatch.setenv("CONTACT_COOLDOWN_MINUTES", "5")
    monkeypatch.setenv("VALIDATE_TWILIO_SIGNATURE", "false")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))

    from app.database import initialize_database

    initialize_database()


@pytest.fixture
def app(test_environment):

    from app import create_app

    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()
