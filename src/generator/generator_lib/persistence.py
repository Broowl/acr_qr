from dataclasses import dataclass
import os
from pathlib import Path
import json
from io import TextIOWrapper


@dataclass
class PersistedValues:
    """Storage for the persisted values"""
    out_dir: Path


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
                        Path(parsed["out_dir"]))
                except json.JSONDecodeError:
                    self._write(file)
        else:
            config_dir = os.path.dirname(self.config_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            with open(self.config_path, "w", encoding="utf-8") as file:
                self._write(file)

    def persist_out_dir(self, out_dir: Path) -> None:
        self.persisted_values.out_dir = out_dir
        with open(self.config_path, "w", encoding="utf-8") as file:
            self._write(file)

    def get_persisted_out_dir(self) -> Path:
        return self.persisted_values.out_dir

    def _write(self, file: TextIOWrapper) -> None:
        serialized = json.dumps(
            {"out_dir": self.persisted_values.out_dir.as_posix()})
        file.write(serialized)
        file.flush()
