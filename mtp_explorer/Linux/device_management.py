import click
import pathlib


def l_list_devices():
    gvfs_path = pathlib.Path("/run/user/1000/gvfs")

    click.echo("CONNECTED DEVICES:")
    for device in enumerate(gvfs_path.iterdir()):
        click.echo(f"{device[0]}. {device[1].name.split('=')[1]}")
