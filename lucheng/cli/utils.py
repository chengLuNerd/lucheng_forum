"""
summary: command line utils.

description: xxxx
"""

import sys
import os
import click
from flask import __version__ as flask_version

from lucheng import __version__
from lucheng.utils.populate import create_user


def get_version(ctx, param, value):
    """Get version information."""
    if not value or ctx.resilient_parsing:
        return
    """
    print(ctx)
    print(param)
    print(value)
    """
    message = (
        "Lucheng %(version)s using Flask %(flask_version)s on "
        "Python %(python_version)s"
    )
    click.echo(message % {
        'version': __version__,
        'flask_version': flask_version,
        'python_version': sys.version.split()[0]
    }, color=ctx.color)


def save_user_prompt(username, email, password, group):
    """Input the user information."""
    if not username:
        username = click.prompt(click.style("username", fg="magenta"),
                                type=str, default=os.environ.get("USER", ""))
    if not email:
        email = click.prompt(click.style("email", fg="magenta"))
    if not password:
        password = click.prompt(click.style("password", fg="magenta"),
                                hide_input=True, confirmation_prompt=True)
    # print(password)
    if not group:
        group = click.prompt(
            click.style("Group", fg="magenta"),
            type=click.Choice(["admin", "super_mode", "mod", "member"]))

    return create_user(username, password, email, group)


def write_config(config, config_template, config_path):
    """Write a new config file based upon the config template.

    :param config: A dict containing all the key/value pairs which should be
                   used for the new configuration file.
    :param config_template: The config (jinja2-)template.
    :param config_path: The place to write the new config file.
    """
    with open(config_path, "wb") as cfg_file:
        cfg_file.write(config_template.render(**config).encode("utf-8"))
