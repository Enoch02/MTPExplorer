import click

import mtp_commands


@click.group()
def cli():
    pass


cli.add_command(mtp_commands.list_devices)
cli.add_command(mtp_commands.find)


if __name__ == "__main__":
    cli()
