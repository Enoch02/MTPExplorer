import datetime
import sys
import threading
import time
from pathlib import Path

import click


def file_preview(files: list[Path]):
    file_names = map(lambda f: f.name, files)
    click.echo_via_pager("\n".join(file_names))


def long_file_preview(files: list[Path]):
    def _format_long_preview(file: Path) -> str:
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

        return (
            f"{file.name.ljust(20)} " f"{size_str.rjust(10)} " f"{last_modified_time}"
        )

    long_names = map(lambda f: _format_long_preview(f), files)
    click.echo_via_pager("\n".join(long_names))


class IndeterminateProgress(threading.Thread):
    def __init__(self):
        super(IndeterminateProgress, self).__init__()
        self._stop_event = threading.Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            for char in "|/-\\":
                sys.stdout.write("\r" + char)
                sys.stdout.flush()
                time.sleep(0.1)

    def stop(self):
        self._stop_event.set()
