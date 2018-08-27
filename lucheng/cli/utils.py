import sys
import click
from flask import __version__ as flask_version

from lucheng import __version__

def get_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    """
    print(ctx)
    print(param)
    print(value)
    """
    message = ("Lucheng %(version)s using Flask %(flask_version)s on "
                "Python %(python_version)s")
    click.echo(message % {
        'version': __version__,
        'flask_version': flask_version,
        'python_version': sys.version.split()[0]
    }, color=ctx.color)
