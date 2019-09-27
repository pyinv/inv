"""Command to list assets."""
import click

from inv.asset_tree import AssetTree
from inv.cli.env import get_inv


@click.command()
def list() -> None:
    """List models."""
    inv = get_inv()
    click.echo("This is not yet implemented.")
    click.echo("Blocked on manufacturers.")
