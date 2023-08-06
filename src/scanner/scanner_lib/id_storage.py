import os
from pathlib import Path
import time
from io import TextIOWrapper
from types import TracebackType
from typing import Dict, Optional, Any


class IdStorage:
    """Class for storing scanned ticket IDs"""

    def __init__(self, log_dir: Path, grace_period_s: int) -> None:
        self.log_dir = log_dir
        self.grace_period_s = grace_period_s
        self.storage: Dict[int, float] = {}
        self.file: Optional[TextIOWrapper] = None

    def __enter__(self) -> Any:
        self._save_open()
        return self

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: TracebackType | None) -> None:
        if self.file is not None:
            self.file.close()

    def try_add_id(self, ticket_id: int) -> bool:
        stored_time = self.storage.get(ticket_id)
        if stored_time is None:
            self._add(ticket_id)
            return True
        return time.time() - stored_time < self.grace_period_s

    def set_dir(self, log_dir: Path) -> None:
        if self.file is not None:
            self.file.close()
        self.log_dir = log_dir
        self._save_open()

    def _add(self, ticket_id: int) -> None:
        if self.file is None:
            return
        now = time.time()
        self.storage[ticket_id] = now
        local_time = time.localtime(now)
        self.file.write(
            f"{local_time.tm_year}-{local_time.tm_mon}-{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec},{ticket_id}\n")
        self.file.flush()

    def _save_open(self) -> None:
        if (not os.path.exists(self.log_dir)):
            os.makedirs(self.log_dir)
        self.file = open(self.log_dir / "ids.txt", "w", encoding="utf-8")
