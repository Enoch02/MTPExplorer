import click
import platform
from Linux.device_management import l_list_devices
from Windows.device_management import w_list_devices


@click.command()
def list_devices():
    """List the mtp devices connected to this computer"""
    match platform.system():
        case "Linux":
            l_list_devices()
        case "Windows":
            w_list_devices()
        case _:
            click.echo("Your system is not supported")


@click.command()
@click.argument("pattern", type=click.STRING)
@click.option("--device", type=click.INT, default=0)
def find(pattern: str, device: int):
    """Find the files that match the specified pattern on a device"""
    pass
