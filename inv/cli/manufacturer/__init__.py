"""Commands to control manufacturers."""
import click

from .create import create
from .list import list


@click.group()
def manufacturer() -> None:
    """Manipulate and view manufacturers."""
    pass


manufacturer.add_command(create)
manufacturer.add_command(list)
