"""Main app file.

manages the app creation and configuration process
"""

import os
from flask import Flask, render_template
from lucheng.forum.views import forum
from lucheng.auth.views import auth
from lucheng.extensions import (db, migrate, login_manager, bootstrap)
from lucheng.user.models import User


def create_app(config=None):
    """App factory function."""
    app = Flask(__name__)

    # configure
    configure_app(app, config)

    # register Blueprint
    configure_blueprint(app)

    configure_extensions(app)

    # error handler
    configure_errorhandlers(app)

    return app


def configure_blueprint(app):
    """App blueprint register."""
    app.register_blueprint(forum)
    app.register_blueprint(auth)


def configure_app(app, config):
    """App configure function."""
    # first import from default configure file
    app.config.from_object('lucheng.configs.default.DefaultConfig')

    # print(app.config)
    if isinstance(config, str) and os.path.exists(os.path.abspath(config)):
        app.config.from_pyfile(os.path.abspath(config))
    else:
        app.config.from_object(config)

    # finally import from env variable
    app.config.from_envvar("LUCHENG_SETTINGS", silent=True)


def configure_errorhandlers(app):
    """App error handlers configure function."""
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500


def configure_extensions(app):
    """App extension configure function."""
    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Flask-Bootstrap
    bootstrap.init_app(app)

    # Flask_Login
    login_manager.init_app(app)

    login_manager.login_view = app.config['LOGIN_VIEW']

    @login_manager.user_loader
    def load_user(user_id):
        """Load the user, Required by the 'login' extension."""
        user_instance = User.query.filter_by(id=user_id).first()
        """
        if user_instance:
            return user_instance
        else:
            return None
        """
        return user_instance
