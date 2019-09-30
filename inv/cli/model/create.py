"""Command to create models."""
import click

from inv.asset_manufacturer import AssetManufacturer
from inv.asset_model import AssetModel
from inv.cli.custom_types import ASSET_MANUFACTURER
from inv.cli.env import get_inv


@click.command()
@click.option('--name', prompt=True, type=click.STRING)
@click.option('--container', prompt=True, type=click.BOOL)
@click.option('--manufacturer', prompt=True, type=ASSET_MANUFACTURER())
def create(name: str, container: bool, manufacturer: AssetManufacturer) -> None:
    """Create a new model."""
    inv = get_inv()

    model = AssetModel.create_instance(
        name=name,
        container=container,
        manufacturer=manufacturer,
    )

    model.save(inv)
