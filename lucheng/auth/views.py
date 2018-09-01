"""
    flaskbb.auth.views
    ~~~~~~~~~~~~~~~~~~

    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import (Blueprint, url_for, redirect, render_template)
from flask_login import (current_user, login_user)
from lucheng.auth.forms import LoginForm


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log the user in."""

    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for("forum.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.login.data, form.password.data)
        login_user(user)
        return redirect(url_for("form.index"))

    return render_template("auth/login.html",  form=form)
