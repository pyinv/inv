"""Command Line Interface for inv."""

import click

from .asset import asset
from .env import load_env
from .validate import validate

@click.group('inv', invoke_without_command=True)
@click.pass_context
def app(ctx: click.Context) -> None:
    """Inventory Software for humans."""
    ctx.obj = load_env()

    if ctx.invoked_subcommand is None:
        click.echo(app.get_help(ctx))


app.add_command(asset)
app.add_command(validate)

if __name__ == "__main__":
    app()
