"""Command Line Interface for inv."""

import click

from .asset import asset


@click.group()
@click.pass_context
def app(ctx: click.Context) -> None:
    """Inventory Software for humans."""
    pass


app.add_command(asset)

if __name__ == "__main__":
    app()
