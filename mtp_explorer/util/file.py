# TODO: handle potential errors
import click
import pathlib
import typing


def get_all_files(
    root: pathlib.Path,
    exclude: list[str],
    extension: str,
) -> typing.Generator[pathlib.Path, None, None]:
    for item in root.iterdir():
        if item.name in exclude:
            continue

        if item.suffix == extension:
            yield item

        if item.is_dir():
            yield from get_all_files(item, exclude, extension)


def copy_all_files(files: list[pathlib.Path], destination: pathlib.Path):
    with click.progressbar(iterable=files, label="Copying files") as bar:
        for user in bar:
            f = destination.joinpath(user.name)
            f.write_bytes(user.read_bytes())
    click.echo(f"All files have been successfully copied to: {destination}")
