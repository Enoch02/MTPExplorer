import pathlib
import platform

import click
from Linux.device_management import l_list_devices
from model.devices import Devices
from util.file import get_all_files, copy_all_files
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


@click.command()
@click.argument("extension", type=click.STRING)
@click.option("--device", type=click.INT, default=0)
@click.option(
    "--exclude",
    multiple=True,
    default=["Android", ".thumbnails", "LOST.DIR"],
)
@click.pass_obj
def find_extension(devices: Devices, extension: str, device: int, exclude: list[str]):
    """List the files that match the specified extension."""
    try:
        device_path = devices.device_paths[device]
        files = list(
            get_all_files(
                root=device_path,
                exclude=exclude,
                extension=extension,
            )
        )

        if (len(files) > 0):
            for file in files:
                click.echo(file.name)

            if click.confirm(f"Do you want to copy {len(files)} files"):
                destination_path = pathlib.Path(
                    click.prompt(
                    text="Enter the destination path",
                    type=click.Path(readable=True),
                    )
                )
                copy_all_files(
                    files=files,
                    destination=destination_path,
                )
        else:
            click.echo(f"'{extension}' files not found on the device.")

    except IndexError:
        click.echo("No device connected!")
    except Exception as e:
        click.echo(e)
