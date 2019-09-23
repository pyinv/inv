"""Commands to control asset."""
import click

from .list_assets import list


@click.group()
def asset() -> None:
    """Manipulate and view assets."""
    pass


asset.add_command(list)
