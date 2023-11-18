import pathlib
import platform

import click
from Linux.device_management import l_list_devices
from model.devices import Devices
from util.file import get_all_files, copy_all_files, delete_all_files
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
@click.option("-d", "--device", type=click.INT, default=0, help="Select device by index")
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    default=["Android", ".thumbnails", "LOST.DIR"],
    help="Specify folder(s) to ignore"
)
@click.option("-x", "--delete", is_flag=True, help="Delete files after copying")
@click.pass_obj
def find_extension(
    devices: Devices,
    extension: str,
    device: int,
    exclude: list[str],
    delete: bool,
):
    """
    List the files that match the specified extension.

    EXTENSION is the extension type to search for [example: .png]
    """
    try:
        device_path = devices.device_paths[device]
        files = list(
            get_all_files(
                root=device_path,
                exclude=exclude,
                extension=extension,
            )
        )

        if len(files) > 0:
            for file in files:
                click.echo(file.name)

            if click.confirm(f"Do you want to copy {len(files)} file(s)"):
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
            if delete:
                delete_all_files(files=files)

        else:
            click.echo(f"'{extension}' files not found on the device.")

    except IndexError:
        click.echo("No device connected!")
    except Exception as e:
        click.echo(e)


# TODO: add command to find folders?
