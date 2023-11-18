import datetime
from pathlib import Path

import click


def file_preview(files: list[Path]):
    for file in files:
        click.echo(file.name)


def long_file_preview(files: list[Path]):
    for file in files:
        file_info = file.stat()
        file_size = file_info.st_size

        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"

        last_modified_time = datetime.datetime.fromtimestamp(
            file_info.st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S")
        click.echo(
            f"{file.name.ljust(20)} " f"{size_str.rjust(10)} " f"{last_modified_time}"
        )
