"""Command to add an asset."""
import click

from inv.asset import Asset
from inv.asset_model import AssetModel
from inv.asset_tree import AssetTree
from inv.cli.custom_types import ASSET_CODE, ASSET_MODEL, ASSET_TREE
from inv.cli.env import get_inv


@click.command()
@click.option('--code', prompt=True, type=ASSET_CODE())
@click.option('--model', prompt=True, type=ASSET_MODEL())
@click.option('--name', prompt=True, type=click.STRING)
@click.option('--location', prompt=True, type=ASSET_TREE())
def add(
        code: str,
        model: AssetModel,
        name: str,
        location: AssetTree,
) -> None:
    """
    Add an asset.

    This command does not generate an asset code.
    """
    inventory = get_inv()

    # Check that the code is unused
    code_check = inventory.find_asset_by_code(code)
    if code_check is not None:
        click.secho(
            f"{inventory.asset_code.human_format(code)} is already in use.",
            fg="red",
            err=True,
        )
        print(f"Name: {code_check.name}")
        print(f"Model: {code_check.model.name}")
        exit(1)
    Asset.save_new(
        code=code,
        model=model,
        name=name,
        location=location,
        inv=inventory,
    )
