from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Class which holds the configurable values of the QR-Code generator"""
    event_name: str
    num_qr_codes: int
    out_dir: Path
    key_dir: Path
