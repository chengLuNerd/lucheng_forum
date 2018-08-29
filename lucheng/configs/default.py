"""default configure define."""

import os


class DefaultConfig(object):
    """default configuration of app."""

    # ../../
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

    DEBUG = True

    SECRET_KEy = 'hard to guess string'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + 'flaskbb.sqlite'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
