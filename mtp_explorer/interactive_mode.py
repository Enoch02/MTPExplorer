import pathlib
import platform
from enum import Enum
from pathlib import Path

import click


class State(Enum):
    SELECTING_DEVICE = 1
    SELECTING_COMMAND = 2
    EXECUTING_COMMAND = 3
    EXITING = -1


class Command(Enum):
    FIND_EXTENSION = "Find extension"
    FIND_PATTERN = "Find pattern"
    EXIT = "Exit"


@click.pass_context
def start_interactive_mode(ctx: click.Context):
    current_state = State.SELECTING_DEVICE
    device: pathlib.Path | None = None
    command: str | None = None

    while True:
        match current_state:
            case State.SELECTING_DEVICE:
                device = choose_device()

                if device is not None:
                    current_state = State.SELECTING_COMMAND

            case State.SELECTING_COMMAND:
                command = choose_command()

                if command is not None:
                    current_state = State.EXECUTING_COMMAND

            case State.EXECUTING_COMMAND:
                match command:
                    case Command.EXIT:
                        current_state = State.EXITING
                    case _:
                        click.secho("NOT IMPLEMENTED", fg="red")
                        ctx.exit(1)

            case State.EXITING:
                ctx.exit(0)


def choose_device() -> Path | None:
    devices: list[pathlib.Path] = []

    match platform.system():
        case "Linux":
            from mtp_explorer.Linux.device_management import l_list_devices

            devices = l_list_devices(show_output=True)
        case "Windows":
            from mtp_explorer.Windows.device_management import w_list_devices

            devices = w_list_devices()
        case _:
            click.echo("Your OS is not supported")

    if len(devices) > 0:
        device = click.prompt("Select a device", type=click.INT, default=0)
        try:
            return devices[device]
        except IndexError:
            click.secho("Error: invalid index.", fg="red")

    return None


def choose_command():
    available_commands = list(Command)

    click.echo("COMMANDS: ")
    for index, command in enumerate(available_commands):
        click.echo(f"{index}.{command.value}")

    selected_command = click.prompt("What do you want to do?", type=click.INT)

    try:
        return available_commands[selected_command]
    except IndexError:
        click.secho("Error: invalid index.", fg="red")
        return None
