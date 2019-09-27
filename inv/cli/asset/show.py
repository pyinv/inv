"""Command to show an asset."""
import click

from inv.asset import Asset
from inv.asset_tree import AssetTree
from inv.cli.custom_types import ASSET_CODE
from inv.cli.env import get_inv


@click.command()
@click.option('--code', prompt=True, type=ASSET_CODE())
def show(code: str) -> None:
    """
    Show information about an asset.

    Will prompt for a code when run without options.

    e.g inv asset show

    e.g inv asset show --code SRO-ABC-DEF
    """
    inventory = get_inv()

    asset = inventory.find_asset_by_code(code)

    if asset is None:
        click.secho(f"Unable to find asset: {code}.", err=True, fg="red")
        exit(1)

    if isinstance(asset, Asset):
        asset.display(inventory)

    if isinstance(asset, AssetTree):
        asset.container.display(inventory)
        print(f"Found: {len(asset.contents)} items in container")
        for i in asset.contents:
            print(f"\t{str(i)}")
