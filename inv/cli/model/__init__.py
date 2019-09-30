"""Commands to control model."""
import click

from .create import create
from .list import list


@click.group()
def model() -> None:
    """Manipulate and view models."""
    pass


model.add_command(create)
model.add_command(list)
