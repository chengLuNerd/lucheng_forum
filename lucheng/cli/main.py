"""
summary: command line define file. support install command.

description: main.py
"""
import click
import sys
import os
import binascii
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from flask import current_app
from flask.cli import FlaskGroup, ScriptInfo
from sqlalchemy_utils.functions import database_exists, create_database
from sqlalchemy_utils.functions import drop_database
from flask_migrate import upgrade as upgrade_database
from lucheng.cli.utils import (get_version, save_user_prompt, write_config)
from lucheng.extensions import db
from lucheng.utils.populate import (create_default_groups, create_welcom_forum)
from lucheng import create_app


def set_config(ctx, param, value):
    """Pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


def make_app(script_info):
    """Create flask app."""
    config_file = getattr(script_info, "config_file")
    return create_app(config_file)


@click.group(cls=FlaskGroup, create_app=make_app, add_version_option=False)
@click.option("--config", expose_value=False, callback=set_config,
              required=False, is_flag=False, is_eager=True, metavar="CONFIG",
              help="Specify the config to use in dotted module notation "
              "e.g. flaskbb.configs.default.DefaultConfig")
@click.option("--version",
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

    if welcome:
        click.secho("[+] Creating welcome forum...", fg="cyan")
        create_welcom_forum()

    click.secho("[+] Lucheng has been successfully installed!",
                fg="green", bold=True)


@lucheng.command("makeconfig")
@click.option("--debug", "-d", default=False, is_flag=True,
              help="Creates a development config with DEBUG set to True.")
@click.option("--output", "-o", default=".",
              help="The path where the config file will be saved at.")
def generate_config(debug, output):
    """
    Generate config file.

    Create a litter wizard which ask you some questions and
    """
    config_env = Environment(
        loader=FileSystemLoader(os.path.join(current_app.root_path, "configs"))
    )
    config_template = config_env.get_template('config.cfg.template')
    if output:
        config_path = os.path.abspath(output)
    else:
        config_path = os.path.dirname(current_app.root_path)

    if os.path.exists(config_path):
        config_path = os.path.join(config_path, "lucheng.cfg")

    database_path = "sqlite:///" + os.path.join(
        os.path.dirname(current_app.instance_path), "flaskbb.sqlite")

    default_conf = {
        "is_debug": False,
        "server_name": "example.org",
        "use_https": True,
        "database_uri": database_path,
        "redis_enabled": False,
        "redis_uri": "redis://localhost:6379",
        "mail_server": "localhost",
        "mail_port": 25,
        "mail_use_tls": False,
        "mail_use_ssl": False,
        "mail_username": "",
        "mail_password": "",
        "mail_sender_name": "FlaskBB Mailer",
        "mail_sender_address": "noreply@yourdomain",
        "mail_admin_address": "admin@yourdomain",
        "secret_key": binascii.hexlify(os.urandom(24)).decode(),
        "csrf_secret_key": binascii.hexlify(os.urandom(24)).decode(),
        "timestamp": datetime.utcnow().strftime("%A, %d. %B %Y at %H:%M"),
        "log_config_path": "",
    }

    click.secho("Redis will be used for things such as the task queue,"
                "caching and rate limiting.", fg="cyan")
    default_conf["redis_enabled"] = click.confirm(
        click.style("Would you like to use redis?", fg="magenta"),
        default=default_conf.get("redis_enabled"))

    if default_conf.get("redis_enabled", False):
        default_conf["redis_uri"] = click.prompt(
            click.style("Redis URI", fg="magenta"),
            default=default_conf.get("redis_uri"))
    else:
        default_conf["redis_uri"] = ""

    click.secho("To use 'localhost' make sure that you have sendmail or\n"
                "anything similar installed. Gmail is also supprted.",
                fg="cyan")
    default_conf["mail_server"] = click.prompt(
        click.style("Mail Server", fg="magenta"),
        default=default_conf.get("mail_server"))
    default_conf["mail_port"] = click.prompt(
        click.style("Mail Server SMTP Port", fg="magenta"),
        default=default_conf.get("mail_port"))
    default_conf["mail_use_ssl"] = click.confirm(
        click.style("Use SSL for sending mails?", fg="magenta"),
        default=default_conf.get("mail_use_ssl"))
    default_conf["mail_username"] = click.prompt(
        click.style("Mail Username", fg="magenta"),
        default=default_conf.get("mail_username"))
    default_conf["mail_password"] = click.prompt(
        click.style("Mail Password", fg="magenta"),
        default=default_conf.get("mail_password"))
    default_conf["mail_sender_name"] = click.prompt(
        click.style("Mail Sender Name", fg="magenta"),
        default=default_conf.get("mail_sender_name"))
    default_conf["mail_sender_address"] = click.prompt(
        click.style("Mail Sender Address", fg="magenta"),
        default=default_conf.get("mail_sender_address"))
    default_conf["mail_admin_address"] = click.prompt(
        click.style("Mail Admin Email", fg="magenta"),
        default=default_conf.get("mail_admin_address"))

    config_path = os.path.join(
        os.path.dirname(current_app.root_path), "lucheng.cfg")
    default_conf["log_config_path"] = click.prompt(
        click.style("Logging config path", fg="magenta"),
        default=default_conf.get("log_config_path"))

    write_config(default_conf, config_template, config_path)

    click.secho("The configuration file has been saved to: {cfg}\n"
                "Feel free to further adjust it as needed."
                .format(cfg=config_path), fg="blue")
    click.secho("Usage: \nflaskbb --config {cfg} run"
                .format(cfg=config_path), fg="green")
