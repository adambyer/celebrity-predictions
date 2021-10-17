from flask import Flask
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
import os
from typing import Union

from .auth import bp
from .db import db
from .models import User

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

    # This is needed for Migrate to see changes.
    # TODO: better way?
    from . import models  # noqa: F401

    with app.app_context():
        # TODO: better way?
        from . import admin

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Union[User, None]:
        return User.query.filter_by(id=user_id).first()

    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index() -> str:
        logged_in = f"You are {'' if current_user.is_authenticated else 'not'} logged in"
        return f"Index page: {logged_in}"

    @app.route("/secured")
    @login_required
    def secured() -> str:
        return "You are logged in."

    return app
