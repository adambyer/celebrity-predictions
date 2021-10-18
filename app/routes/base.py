from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("base", __name__, url_prefix="/")


@bp.route("/")
def index() -> str:
    return render_template("index.html")


@bp.route("/secured")
@login_required
def secured() -> str:
    return "You are logged in."
