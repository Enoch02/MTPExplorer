import pathlib
import platform

import click
from Linux.device_management import l_list_devices
from model.devices import Devices
from util.display import file_preview, long_file_preview
from util.file import copy_all_files, delete_all_files, get_all_files
from Windows.device_management import w_list_devices


@click.command()
def list_devices():
    """List the mtp devices connected to this computer."""
    match platform.system():
        case "Linux":
            l_list_devices(show_output=True)
        case "Windows":
            w_list_devices()
        case _:
            click.echo("Your OS is not supported")


# TODO: add verbose output when searching
@click.command()
@click.argument("extension", type=click.STRING)
@click.option(
    "-d", "--device", type=click.INT, default=0, help="Select device by index."
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    default=["Android", ".thumbnails", "LOST.DIR", "cache"],
    help="Specify folder(s) to ignore.",
)
@click.option("-x", "--delete", is_flag=True, help="Delete files after copying.")
@click.option("-l", "--long", is_flag=True, help="Display files in long format.")
@click.pass_obj
def find_extension(
        devices: Devices,
        extension: str,
        device: int,
        exclude: list[str],
        delete: bool,
        long: bool,
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
            match long:
                case True:
                    long_file_preview(files)
                case False:
                    file_preview(files)

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
            click.secho(f"'{extension}' files not found on the device.", fg="red")

    except IndexError:
        click.secho("No device connected!", fg="red")
    except Exception as e:
        click.echo(e)


@click.command()
@click.argument("pattern", type=click.STRING)
@click.option("-d", "--device", type=click.INT, default=0, help="Select device by index.")
@click.pass_obj
def find_pattern(devices: Devices, pattern: str):
    """
    List the files that match the specified pattern.

    PATTERN is the regex pattern to search for []
    """
    """try:
        device_path = devices.device_paths[device]
        files = list(
            get_all_files(
                root=device_path
            )
        )
    except"""
    pass

# TODO: add command to find folders?
