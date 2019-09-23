"""Code for loading the environment."""
import importlib.util
from typing import no_type_check

import click

from inv import Inventory


@no_type_check
def load_env() -> Inventory:
    """Load the inventory config and environment."""

    try:
        spec = importlib.util.spec_from_file_location("config", "config.py")
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
    except FileNotFoundError:
        click.secho("Unable to find inventory config.", err=True, fg="red")
        exit(1)

    return config.inventory
