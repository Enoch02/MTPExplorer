# TODO: handle potential errors

import click
import pathlib
import typing

from mtp_explorer.util.display import IndeterminateProgress


def get_all_files(
    root: pathlib.Path,
    exclude: list[str],
    extension: str,
    progress_thread=None,
    depth=0,
) -> typing.Generator[pathlib.Path, None, None]:
    if progress_thread is None:
        progress_thread = IndeterminateProgress()
        progress_thread.start()

    for item in root.iterdir():
        if item.name in exclude:
            continue

        if item.suffix == extension:
            yield item

        if item.is_dir():
            yield from get_all_files(
                item, exclude, extension, progress_thread, depth + 1
            )
    else:
        if depth == 0:
            progress_thread.stop()


def copy_all_files(files: list[pathlib.Path], destination: pathlib.Path):
    overwrite_others = False

    with click.progressbar(iterable=files, label="Copying files") as bar:
        for file in bar:
            destination_file = destination.joinpath(file.name)

            match destination_file.exists():
                case True:
                    if overwrite_others:
                        destination_file.write_bytes(file.read_bytes())
                    else:
                        if click.confirm(
                            f"\n`{file.name}` exists at the destination, do you wish to overwrite it?"
                        ):
                            destination_file.write_bytes(file.read_bytes())

                        overwrite_others = click.confirm(
                            "Do you want to apply this choice to the remaining files?"
                        )

                case False:
                    destination_file.write_bytes(file.read_bytes())

    click.echo(f"All files have been successfully copied to: {destination}")


def delete_all_files(files: list[pathlib.Path]):
    with click.progressbar(iterable=files, label="Deleting files from device") as bar:
        for file in bar:
            file.unlink()
