"""Command to list assets."""
import click

from inv.asset_manufacturer import AssetManufacturer
from inv.cli.env import get_inv


@click.command()
def list() -> None:
    """List models."""
    inv = get_inv()

    mans = AssetManufacturer.get_all(inv)

    for man in mans:
        print(f"{man.name}({man.path.name})")
        for model in man.get_models(inv):
            print(f" - {model.name}({model.path.stem})")
