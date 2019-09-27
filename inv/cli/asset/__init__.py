"""Commands to control asset."""
import click

from .edit import edit
from .list_assets import list
from .move import move
from .show import show


@click.group()
def asset() -> None:
    """Manipulate and view assets."""
    pass


asset.add_command(edit)
asset.add_command(list)
asset.add_command(move)
asset.add_command(show)
