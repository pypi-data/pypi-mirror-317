from .qt import QSettings
from .options import *


class PortableSettings(QSettings):
    settings_file_path = 'settings.ini'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            self.settings_file_path,
            QSettings.IniFormat,
            *args,
            **kwargs,
        )

    @staticmethod
    def _install() -> None:
        PortableSettings.settings_file_path = (OPTIONS.config_dir / 'settings.ini').as_posix()
