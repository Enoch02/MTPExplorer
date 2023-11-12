import click
import pathlib


@click.command()
def list_devices():
    """List the mtp devices connected to this computer"""
    gvfs_path = pathlib.Path("/run/user/1000/gvfs")

    click.echo("CONNECTED DEVICES:")
    for device in enumerate(gvfs_path.iterdir()):
        click.echo(f"{device[0]}. {device[1].name.split('=')[1]}")


@click.command()
@click.argument("pattern", type=click.STRING)
@click.option("--device", type=click.INT, default=0)
def find(pattern: str, device: int):
    """Find the files that match the specified pattern on a device"""
    pass
