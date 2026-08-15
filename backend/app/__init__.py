from flask import Flask

from .database import initialize_database


def create_app() -> Flask:
    app = Flask(__name__)
    initialize_database()

    from .routes.whatsapp import whatsapp_blueprint
    app.register_blueprint(whatsapp_blueprint)

    return app
