import click
from flask.cli import FlaskGroup, ScriptInfo
from lucheng.cli.utils import get_version
from lucheng import create_app

def set_config(ctx, param, value):
    """This will pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value

def make_app(script_info):
    config_file = getattr(script_info, "config_file")
    return create_app(config_file)

@click.group(cls=FlaskGroup, create_app=make_app, add_version_option=False)
@click.option("--config", expose_value=False, callback=set_config,
            required=False, is_flag=False, is_eager=True, metavar="CONFIG",
            help="Specify the config to use in dotted module notation "
                "e.g. flaskbb.configs.default.DefaultConfig")
@click.option("--version", expose_value=False, callback=get_version,
            is_flag=True, is_eager=True, help="Show the lucheng version")
def lucheng():
    """This is the command interface for lucheng"""
    pass

@lucheng.command()
def install():
    """
    Install lucheng. If no arguments are used, an interactive setup will be run.
    """
    click.secho("[+] Install Lucheng...", fg="cyan")
