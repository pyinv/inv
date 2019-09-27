"""Command to list assets."""
import click

from inv.asset_tree import AssetTree
from inv.cli.env import load_env


def list_contents(tree: AssetTree) -> None:
    """List the contents of a tree."""
    for item in tree.contents:
        if isinstance(item, AssetTree):
            print(item.container)
            list_contents(item)
        else:
            print(item)


@click.command()
def list() -> None:
    """List assets."""
    inventory = load_env()
    list_contents(inventory.tree)
