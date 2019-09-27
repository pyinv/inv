"""Command to edit an asset."""
from pathlib import Path
from shutil import move
from typing import cast

import click
from pydantic import ValidationError

from inv.asset import Asset
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
    else:  # AssetTree
        file = asset.container.path

    data = file.open('r').read()

    click.edit(filename=cast(str, file.resolve()))

    try:
        new_asset = Asset.load_from_file(file, inventory, ignore_filename=True)
        if isinstance(asset, Asset):
            if new_asset.asset_code != asset.asset_code:
                # In future, just hold a copy of the old object
                file.open('w').write(data)
                click.secho(
                    "You are not allowed to edit the asset code.",
                    err=True,
                    fg='red',
                )
                exit(1)

            new_path = file.parent.joinpath(f"{new_asset.calculate_filename()}.yml")
            move(file, new_path)
        else:
            folder = file.parent
            if new_asset.asset_code != asset.container.asset_code:
                # In future, just hold a copy of the old object
                file.open('w').write(data)
                click.secho(
                    "You are not allowed to edit the asset code.",
                    err=True,
                    fg='red',
                )
                exit(1)

            move(folder, folder.parent.joinpath(new_asset.calculate_filename()))

    except ValidationError as e:
        # In future, just hold a copy of the old object
        # Remove duplicate code too!
        file.open('w').write(data)
        click.secho("Invalid data.", err=True, fg='red')
        click.secho(str(e), err=True, fg='red')
        exit(1)
