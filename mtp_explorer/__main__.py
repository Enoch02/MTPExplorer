import click

import mtp_commands
from mtp_explorer.interactive_mode import start_interactive_mode
from mtp_explorer.model import devices


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj = devices.Devices()

    if ctx.invoked_subcommand is None:
        click.echo("Welcome to MTPExplorer interactive mode")
        start_interactive_mode()


cli.add_command(mtp_commands.list_devices)
cli.add_command(mtp_commands.find_extension)
cli.add_command(mtp_commands.find_pattern)

if __name__ == "__main__":
    cli()
