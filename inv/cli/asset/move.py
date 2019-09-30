"""Command to move an asset."""
import shutil
from typing import List, Union

import click

from inv.asset import Asset
from inv.asset_tree import AssetTree
from inv.cli.custom_types import ASSET_CODE
from inv.cli.env import get_inv


@click.command()
@click.option('--destination', prompt=True, type=ASSET_CODE())
def move(destination_code: str) -> None:
    """
    Move an asset.

    Will prompt for codes when run without options.
    """
    inventory = get_inv()

    destination = inventory.find_asset_by_code(destination_code)

    if destination is None:
        click.secho(
            f"Unable to find destination: {destination_code}.",
            err=True,
            fg="red",
        )
        exit(1)

    # Check if container

    if not isinstance(destination, AssetTree):
        click.secho("Destination must be a container.", err=True, fg="red")
        exit(1)
    else:

        click.echo(f"Scan items to move to "
                   f"{destination.container.name} "
                   f"({destination.container.asset_code}).")
        click.echo(f"Scan the destination again to finish.")

        # If moving container, move contents too!
        loop = True
        source_assets: List[Union[AssetTree, Asset]] = []
        while loop:
            data = click.prompt("Asset to move", type=ASSET_CODE())
            asset = inventory.find_asset_by_code(data)

            if isinstance(asset, Asset):
                ac = asset.asset_code
            elif isinstance(asset, AssetTree):
                ac = asset.container.asset_code

            if asset is None:
                click.secho(f"Unable to find {data}.", err=True, fg="red")
            elif ac == destination.container.asset_code:
                loop = False
            else:
                if isinstance(asset, AssetTree):
                    if destination.asset_code in map(
                            lambda x: x.asset_code, asset.contents,
                    ):
                        click.secho(
                            f"Unable to move parent of asset into asset.",
                            err=True,
                            fg="red",
                        )
                    else:
                        source_assets.append(asset)
                else:
                    source_assets.append(asset)

        click.echo("Moving assets.")

        for source in source_assets:
            if isinstance(source, AssetTree):
                print(
                    f"Moving asset {source.container.name}"
                    f"({source.container.asset_code}) and contents "
                    f"to {destination.container.name}"
                    f"({destination.container.asset_code})",
                )
            else:
                print(
                    f"Moving asset {source.name}({source.asset_code})"
                    f" to {destination.container.name}"
                    f"({destination.container.asset_code})",
                )
            shutil.move(source.path, destination.path.joinpath(source.path.name))
