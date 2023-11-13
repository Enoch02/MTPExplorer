import click
import pathlib


def w_list_devices() -> list[pathlib.Path]:
    click.echo("Your OS is not supported")
