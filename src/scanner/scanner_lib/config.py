from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Class which holds the configurable values of the QR-Code scanner"""
    log_dir: Path
    key_path: Path
    