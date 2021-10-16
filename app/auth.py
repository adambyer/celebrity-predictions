from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import functools
from werkzeug.security import check_password_hash, generate_password_hash

from .db import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
    else:
        g.user = None


@bp.route("/register", methods=("GET", "POST"))
def register():
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
                user = User(username=username, password=password, email_address=email_address)
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                error = f"User {username} is already registered."
                print("*** register", str(e))
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = "Incorrect username or password."
        user = User.query.filter(
            (User.username == username) | (User.email_address == username),
        ).first()

        if user and check_password_hash(user.password, password):
            error = None

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
