from importlib import import_module

import click

from plain.runtime import settings


@click.group()
def cli():
    """Sessions management commands."""
    pass


@cli.command()
def clear_expired():
    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except NotImplementedError:
        raise NotImplementedError(
            f"Session engine '{settings.SESSION_ENGINE}' doesn't support clearing expired "
            "sessions."
        )
