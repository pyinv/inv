"""Command to list manufacturers."""
import click

from inv.asset_manufacturer import AssetManufacturer
from inv.cli.env import get_inv

@click.command()
def list() -> None:
    """List manufacturers."""
    inv = get_inv()

    for entry in inv.meta_dir.iterdir():
        if entry.is_dir():
            data_file = entry.joinpath("data.yml")
            man = AssetManufacturer.load_from_file(entry, inv)
            print(f"{entry.name}: {man.name}")
