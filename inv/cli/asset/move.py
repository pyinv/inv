"""Command to move an asset."""
from pathlib import Path

import click
from pydantic import ValidationError

from inv.asset import Asset
from inv.asset_tree import AssetTree
from inv.cli.custom_types import ASSET_CODE
from inv.cli.env import get_inv


@click.command()
@click.option('--destination', prompt=True, type=ASSET_CODE())
def move(destination: str) -> None:
    """
    Move an asset.

    Will prompt for codes when run without options.
    """
    inventory = get_inv()

    destination = inventory.find_asset_by_code(destination)

    if destination is None:
        click.secho(f"Unable to find destination: {destination}.", err=True, fg="red")
        exit(1)

    # Check if container

    click.echo(f"Scan items to move to {destination.container.name} ({destination.container.asset_code}).")
    click.echo(f"Scan the destination again to finish.")

    # If moving container, move contents too!
    loop = True
    while loop:
        data = click.prompt("Asset to move", type=ASSET_CODE())

    click.echo("Moving assets.")
