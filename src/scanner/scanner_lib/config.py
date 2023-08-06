from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    log_dir: Path
    key_path: Path