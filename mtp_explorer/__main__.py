import click

import mtp_commands
from mtp_explorer.model import devices


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj = devices.Devices()


cli.add_command(mtp_commands.list_devices)
cli.add_command(mtp_commands.find_extension)


if __name__ == "__main__":
    cli()
