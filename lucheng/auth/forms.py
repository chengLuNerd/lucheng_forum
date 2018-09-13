"""
lucheng.auth.forms .

It provides the forms that are needed for the auth views.

:copyright: (c) 2014 by the FlaskBB Team.
:license: BSD, see LICENSE for more details.
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Login Form define."""

    login = StringField("Username or Email address", validators=[
        DataRequired(message="Please enter your username or email address.")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(message="Please enter your password.")
    ])

    remember_me = BooleanField("Remember me", default=False)

    submit = SubmitField("Login")
