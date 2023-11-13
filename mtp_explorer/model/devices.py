import platform
from Linux.device_management import l_list_devices
from Windows.device_management import w_list_devices
from pathlib import Path


class Devices(object):
    def __init__(self) -> None:
        self.platform: str = platform.system()
        self.device_paths: list[Path] = self._get_devices(self.platform)

    def _get_devices(self, platform: str):
        match platform:
            case "Linux":
                return l_list_devices(show_output=False)
            case "Windows":
                return w_list_devices()
            case _:
                return []
