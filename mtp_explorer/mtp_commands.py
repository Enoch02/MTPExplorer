import pathlib
import platform
import re

import click
from Linux.device_management import l_list_devices
from model.devices import Devices
from Windows.device_management import w_list_devices


@click.command()
def list_devices():
    """List the mtp devices connected to this computer"""
    match platform.system():
        case "Linux":
            l_list_devices(show_output=True)
        case "Windows":
            w_list_devices()
        case _:
            click.echo("Your OS is not supported")


# TODO: create option that searches for accepts extensions to search for.
# TODO: work on how to handle patterns later
@click.command()
@click.argument("pattern", type=click.STRING)
@click.option("--device", type=click.INT, default=0)
@click.option("--extension", type=click.STRING)
@click.option(
    "--exclude",
    multiple=True,
    default=["Android", ".thumbnails", "LOST.DIR"],
)
@click.pass_obj
def find(devices: Devices, pattern: str, device: int, exclude: list[str]):
    """Find the files that match the specified pattern on a device"""
    try:
        device_path = devices.device_paths[device]
        files = list(get_all_items(device_path, exclude, pattern))

        for file in files:
            click.echo(file)
    except IndexError:
        click.echo("No device connected!")


def get_all_items(root: pathlib.Path, exclude: list[str], extension: str):
    for item in root.iterdir():
        if item.name in exclude:
            continue

        if item.suffix == extension:
            yield item

        if item.is_dir():
            yield from get_all_items(item, exclude, extension)
