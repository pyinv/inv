"""Command to create manufacturers."""
import click

from inv.asset_manufacturer import AssetManufacturer
from inv.cli.env import get_inv


@click.command()
@click.option('--name', prompt=True, type=click.STRING)
def create(name: str) -> None:
    """Create a new manufacturer."""
    inv = get_inv()

    instance = AssetManufacturer.create_instance(inv, name)

    try:
        instance.save(inv)
    except FileExistsError:
        click.secho(
            "Manufacturer with that name already exists.",
            fg="red",
            err=True,
        )
        exit(1)
    click.echo(f"Created {name}")
