from app import create_app
from app.config import load_config


def main() -> None:
    config = load_config()
    app = create_app()
    app.config["ENV"] = config["FLASK_ENV"]
    app.config["DEBUG"] = config["FLASK_ENV"].lower() == "development"

    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])


if __name__ == "__main__":
    main()
