"""Commands to control asset."""
import click

from .add import add
from .edit import edit
from .list import list
from .move import move
from .show import show


@click.group()
def asset() -> None:
    """Manipulate and view assets."""
    pass


asset.add_command(add)
asset.add_command(edit)
asset.add_command(list)
asset.add_command(move)
asset.add_command(show)
