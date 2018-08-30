"""
summary: command line define file. support install command.

description: main.py
"""
import click
import sys

from flask.cli import FlaskGroup, ScriptInfo
from sqlalchemy_utils.functions import database_exists, create_database
from sqlalchemy_utils.functions import drop_database
from flask_migrate import upgrade as upgrade_database
from lucheng.cli.utils import (get_version, save_user_prompt)
from lucheng.extensions import db
from lucheng.utils.populate import create_default_groups
from lucheng import create_app


def set_config(ctx, param, value):
    """Pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


def make_app(script_info):
    """Create flask app."""
    config_file = getattr(script_info, "config_file")
    return create_app(config_file)


@click.group(cls=FlaskGroup, create_app=make_app, add_version_option=False)
@click.option(
            "--config", expose_value=False, callback=set_config,
            required=False, is_flag=False, is_eager=True, metavar="CONFIG",
            help="Specify the config to use in dotted module notation "
            "e.g. flaskbb.configs.default.DefaultConfig")
@click.option(
            "--version",
            expose_value=False, callback=get_version,
            is_flag=True, is_eager=True, help="Show the lucheng version")
def lucheng():
    """Command interface for lucheng."""
    pass


@lucheng.command()
@click.option("--welcome", "-w", default=True, is_flag=True,
              help="Disable the welcome forum.")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Doesn't ask for confirmation.")
@click.option("--username", "-u", help="The username of the user.")
@click.option("--email", "-e", help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
@click.option("--group", "-g", help="The group of the user.",)
def install(welcome, force, username, email, password, group):
    """
    Install lucheng.

    If no arguments are used, an interactive setup will be run.
    """
    click.secho("[+] Install Lucheng...", fg="cyan")
    if database_exists(db.engine.url):
        if force or click.confirm(click.style(
            "Existing database found. Do you want to delete the old one and "
            "create a new one?", fg="magenta")
        ):
            drop_database(db.engine.url)
        else:
            sys.exit(0)
    create_database(db.engine.url)
    upgrade_database()

    click.secho("[+] Creating default settings...", fg="cyan")
    create_default_groups()
    # create_default_settings()

    click.secho("[+] Creating admin user...", fg="cyan")
    save_user_prompt(username, email, password, group)

    click.secho("[+] Lucheng has been successfully installed!",
                fg="green", bold=True)
