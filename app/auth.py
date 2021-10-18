from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_user, logout_user
from typing import Union
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers import Response

from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register() -> Union[str, Response]:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email_address = request.form["email_address"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                password = generate_password_hash(password)
                user = User(
                    username=username, password=password, email_address=email_address
                )
                user.save()
            except Exception as e:
                error = f"User {username} is already registered."
                print("*** register", str(e))
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> Union[str, Response]:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error: Union[str, None] = "Incorrect username or password."
        user = User.query.filter(
            (User.username == username) | (User.email_address == username),
        ).first()

        if user and check_password_hash(user.password, password):
            error = None

        if error is None:
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("index"))
