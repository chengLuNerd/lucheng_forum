"""
all extensions put here.

The extensions that are used by lucheng
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Database
db = SQLAlchemy()

# Migrations
migrate = Migrate()
