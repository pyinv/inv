"""Command to list manufacturers."""
import click

from inv.asset_manufacturer import AssetManufacturer
from inv.cli.env import get_inv


@click.command()
def list() -> None:
    """List manufacturers."""
    inv = get_inv()

    for entry in AssetManufacturer.get_all(inv):
        print(f"{entry.name}")
