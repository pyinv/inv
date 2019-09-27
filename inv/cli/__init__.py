"""Command Line Interface for inv."""

import click

from .asset import asset
from .env import load_env


@click.group('inv', invoke_without_command=True)
@click.pass_context
def app(ctx: click.Context) -> None:
    """Inventory Software for humans."""
    ctx.obj = load_env()

    if ctx.invoked_subcommand is None:
        click.echo('Found inventory config')
        click.secho('Nothing is implemented here.', err=True, fg="red")


app.add_command(asset)

if __name__ == "__main__":
    app()
