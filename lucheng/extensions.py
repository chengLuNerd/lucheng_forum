"""
all extensions put here.

The extensions that are used by lucheng
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


# Database
db = SQLAlchemy()

# Migrations
migrate = Migrate()

# Login
login_manager = LoginManager()

bootstrap = Bootstrap()
