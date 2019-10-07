"""Command to list assets."""
import click

from inv.asset_tree import AssetTree
from inv.cli.env import get_inv


def list_contents(tree: AssetTree, depth: int = 0) -> None:
    """List the contents of a tree."""
    dstring = '\t' * depth
    for item in tree.contents:
        if isinstance(item, AssetTree):
            print(f"{dstring}{item.asset_code} - {item.model.full_name} - {item.name}")
            list_contents(item, depth + 1)
        else:
            print(f"{dstring}{item.asset_code} - {item.model.full_name} - {item.name}")


@click.command()
def list() -> None:
    """List assets."""
    inv = get_inv()
    list_contents(inv.tree)
