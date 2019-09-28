"""Commands to control manufacturers."""
import click

from .list import list


@click.group()
def manufacturer() -> None:
    """Manipulate and view manufacturers."""
    pass

manufacturer.add_command(list)
