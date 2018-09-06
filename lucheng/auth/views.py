"""
flaskbb.auth.views .

This view provides user authentication, registration and a view for
resetting the password of a user if he has lost his password

"""
from flask import (Blueprint, url_for, redirect, render_template, flash)
from flask_login import (current_user, login_user)
from lucheng.auth.forms import LoginForm
from lucheng.user.models import User
from lucheng.extensions import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log the user in."""
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("forum.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.\
            filter(db.or_(User.username == form.login.data,
                   User.email == form.login.data)).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("forum.index"))
            flash("Invalid username or password", category="danger")
    return render_template("auth/login.html", form=form)
