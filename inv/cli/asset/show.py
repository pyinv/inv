"""Command to show an asset."""
import click

from inv.asset_tree import AssetTree
from inv.cli.env import load_env
from inv.cli.custom_types import DAMM32


def list_contents(tree: AssetTree) -> None:
    """List the contents of a tree."""
    for item in tree.contents:
        if isinstance(item, AssetTree):
            print(item.container)
            list_contents(item)
        else:
            print(item)


@click.command()
@click.option('--code', prompt=True, type=DAMM32("ABC"))  # Hard-coded :/
def show(code: str) -> None:
    """
    Show information about an asset.

    Will prompt for a code when run without options.

    e.g inv asset show

    e.g inv asset show --code SRO-ABC-DEF
    """
    inventory = load_env()
    print(code)
