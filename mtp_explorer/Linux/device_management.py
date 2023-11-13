import click
import pathlib


def l_list_devices(show_output=False) -> list[pathlib.Path]:
    gvfs_path = pathlib.Path("/run/user/1000/gvfs")
    devices = list(gvfs_path.iterdir())

    if show_output:
        if (len(devices) > 0):
            click.echo("CONNECTED DEVICES:")
            for device in enumerate(devices):
                click.echo(f"{device[0]}. {device[1].name.split('=')[1]}")
        else:
            click.echo("NO DEVICE FOUND.")
            click.echo("Please check the usb connection.")
            
    return devices
