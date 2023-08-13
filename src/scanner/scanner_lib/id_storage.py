import os
from pathlib import Path
import time
import csv
from datetime import datetime, timezone
from io import TextIOWrapper
from types import TracebackType
from typing import Dict, Optional, Any
import iso8601
from .persistence import Persistence


class IdStorage:
    """Class for storing scanned ticket IDs"""

    def __init__(self, log_dir: Path, grace_period_s: int, persistence: Persistence) -> None:
        self.log_dir = log_dir
        self.grace_period_s = grace_period_s
        self.storage: Dict[int, float] = {}
        self.file: Optional[TextIOWrapper] = None
        self.writer: Optional[Any] = None
        self.persistence = persistence
        self.event_name = "default"

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
        self.persistence.persist_log_dir(log_dir)

    def set_event_name(self, event_name: str) -> None:
        self.event_name = event_name
        if self.file is not None:
            self.file.close()
        self._save_open()

    def _add(self, ticket_id: int) -> None:
        if self.file is None or self.writer is None:
            return
        now = time.time()
        # inequality to now is fine here
        time_stamp = datetime.now(timezone.utc).isoformat()
        self.storage[ticket_id] = now
        self.writer.writerow([time_stamp, ticket_id])
        self.file.flush()

    def _save_open(self) -> None:
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        file_name = self.log_dir / f"{self.event_name}.txt"
        # restore IDs from if log with the current event name exists and is less than 1 day old
        if os.path.exists(file_name) and time.time() - os.stat(file_name).st_mtime < 60*60*24:
            self.file = open(file_name, "r+", encoding="utf-8")
            self._read_file()
        else:
            self.file = open(file_name, "w", encoding="utf-8")
        self.writer = csv.writer(self.file, delimiter=',')

    def _read_file(self) -> None:
        if self.file is not None:
            id_reader = csv.reader(self.file, delimiter=',')
            for row in id_reader:
                if len(row) != 0:
                    date_time = iso8601.parse_date(row[0])
                    epoch = datetime.fromtimestamp(0, timezone.utc)
                    self.storage[int(row[1])] = (
                        date_time - epoch).total_seconds()
