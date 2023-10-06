from dataclasses import dataclass
from pathlib import Path
from datetime import date


@dataclass
class Config:
    """Class which holds the configurable values of the QR-Code generator"""
    event_name: str
    event_date: date
    num_qr_codes: int
    out_dir: Path
    private_key_path: Path
    flyer_file_name: Path | None
