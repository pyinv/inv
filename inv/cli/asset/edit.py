"""Command to edit an asset."""
from pathlib import Path

import click
from pydantic import ValidationError

from inv.asset import Asset
from inv.asset_tree import AssetTree
from inv.cli.custom_types import ASSET_CODE
from inv.cli.env import get_inv


@click.command()
@click.option('--code', prompt=True, type=ASSET_CODE())
def edit(code: str) -> None:
    """
    Edit an asset.

    Will prompt for a code when run without options.

    e.g inv asset edit

    e.g inv asset edit --code SRO-ABC-DEF
    """
    inventory = get_inv()

    asset = inventory.find_asset_by_code(code)

    if asset is None:
        click.secho(f"Unable to find asset: {code}.", err=True, fg="red")
        exit(1)

    file = Path()

    if isinstance(asset, Asset):
        file = asset.path
    elif isinstance(asset, AssetTree):
        file = asset.container.path

    data = file.open('r').read()

    click.edit(filename=file)

    try:
        Asset.load_from_file(file)
    except ValidationError as e:
        file.open('w').write(data)
        click.secho("Invalid data.", err=True, color="red")
        click.secho(str(e), err=True, color="red")
        exit(1)
