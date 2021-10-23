from flask import Flask
# from flask_login import LoginManager
from flask_migrate import Migrate
import os
from typing import Union

# from .routes.auth import bp as auth_bp
# from .routes.base import bp as base_bp
# from .routes.celebrity import bp as celebrity_bp
from .db import db
# from .models import User

migrate = Migrate(compare_type=True)

# This will be overridden by an environment variable in prod.
SECRET_KEY = "d8ce4cde7950de5b9dd0093beca9aa59156f094354721165d0b5505f3c43633d"


def create_app(test_config: dict = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", SECRET_KEY),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="postgresql://localhost/celebrity_predictions",
    )

    # TODO: better way than importing all this stuff here??
    from . import events  # noqa: F401

    with app.app_context():
        from . import admin  # noqa: F401

    # app.register_blueprint(auth_bp)
    # app.register_blueprint(base_bp)
    # app.register_blueprint(celebrity_bp)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
