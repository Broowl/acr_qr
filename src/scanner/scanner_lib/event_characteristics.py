from dataclasses import dataclass
from datetime import date


@dataclass
class EventCharacteristics:
    """Data characterizing the event"""
    name: str
    date: date
