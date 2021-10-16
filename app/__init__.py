from flask import Flask
from flask_migrate import Migrate

from .auth import bp
from .db import db

migrate = Migrate(compare_type=True)


def create_app(test_config: dict = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="postgresql://localhost/celebrity_predictions",
    )

    # This is needed for Migrate to see changes.
    from . import models  # noqa: F401

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index() -> str:
        return "TEST"

    return app
