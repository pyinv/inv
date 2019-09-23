"""Command to list assets."""
import click

from inv.cli.env import load_env


@click.command()
def list() -> None:
    """List assets."""
    inventory = load_env()
    print(inventory.tree)
