from flask import Flask
import os

# This is needed for Admin to create tasks.
from ..celery import app as celery_app  # noqa: F401


# This will be overridden by an environment variable in prod.
SECRET_KEY = "d8ce4cde7950de5b9dd0093beca9aa59156f094354721165d0b5505f3c43633d"


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", SECRET_KEY),
    )

    with app.app_context():
        from . import admin  # noqa: F401

    return app
