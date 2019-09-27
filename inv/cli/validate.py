"""Command to validate the inventory."""
import click
from typing import List, Callable

from inv import Inventory
from inv.cli.env import get_inv


def validate_inventory_config(inv: Inventory) -> None:
    """Validate the inventory config"""
    assert inv.root_path.exists()
    assert inv.org != ""
    assert inv.root_path.joinpath(inv.meta_dir).exists()


def validate_file_names(inv: Inventory) -> None:
    """Validate that the file names are valid."""
    pass

sections: List[Callable[[Inventory], None]] = [
    validate_inventory_config,
    validate_file_names,
]


@click.command()
def validate() -> None:
    """Validate the inventory."""
    inv = get_inv()
    click.secho(f"Validating inventory at {inv.root_path.resolve()}")

    with click.progressbar(sections) as sections_bar:
        for section in sections_bar:
            section(inv)
