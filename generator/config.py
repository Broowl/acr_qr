from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    event_name: str
    num_qr_codes: int
    out_dir: Path
    key_dir: Path
