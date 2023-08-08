from dataclasses import dataclass
import os
from pathlib import Path
import json
from io import TextIOWrapper


@dataclass
class PersistedValues:
    """Storage for the persisted values"""
    log_dir: Path
    key_path: Path
    camera_index: int


class Persistence:
    """Class for storing scanned ticket IDs"""

    def __init__(self, config_path: Path, default: PersistedValues) -> None:
        self.config_path = config_path
        self.persisted_values = default
        self._do_int()

    def _do_int(self) -> None:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r+", encoding="utf-8") as file:
                try:
                    content = file.read()
                    parsed = json.loads(content)
                    self.persisted_values = PersistedValues(
                        Path(parsed["log_dir"]), Path(parsed["key_path"]), int(parsed["camera_index"]))
                except json.JSONDecodeError:
                    self._write(file)
        else:
            config_dir=os.path.dirname(self.config_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            with open(self.config_path, "w", encoding = "utf-8") as file:
                self._write(file)

    def persist_log_dir(self, log_dir: Path) -> None:
        self.persisted_values.log_dir=log_dir
        with open(self.config_path, "w", encoding = "utf-8") as file:
            self._write(file)

    def persist_key_path(self, key_path: Path) -> None:
        self.persisted_values.key_path=key_path
        with open(self.config_path, "w", encoding = "utf-8") as file:
            self._write(file)

    def persist_camera_index(self, camera_index: int) -> None:
        self.persisted_values.camera_index=camera_index
        with open(self.config_path, "w", encoding = "utf-8") as file:
            self._write(file)

    def get_persisted_log_dir(self) -> Path:
        return self.persisted_values.log_dir

    def get_persisted_key_path(self) -> Path:
        return self.persisted_values.key_path

    def get_persisted_camera_index(self) -> int:
        return self.persisted_values.camera_index

    def _write(self, file: TextIOWrapper) -> None:
        serialized=json.dumps(
            {
                "log_dir": self.persisted_values.log_dir.as_posix(),
                "key_path": self.persisted_values.key_path.as_posix(),
                "camera_index": self.persisted_values.camera_index,
            })
        file.write(serialized)
        file.flush()
