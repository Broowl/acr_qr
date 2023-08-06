import time
from io import TextIOWrapper
from types import TracebackType
from typing import Dict, Optional, Any

# pyright: reportUndefinedVariable=false


class IdStorage:
    """Class for storing scanned ticket IDs"""

    def __init__(self, file_name: str, grace_period_s: int) -> None:
        self.file_name = file_name
        self.grace_period_s = grace_period_s
        self.storage: Dict[int, float] = {}
        self.file: Optional[TextIOWrapper] = None

    def __enter__(self) -> Any:
        self.file = open(self.file_name, "w", encoding="utf-8")
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

    def _add(self, ticket_id: int) -> None:
        if self.file is None:
            return
        now = time.time()
        self.storage[ticket_id] = now
        local_time = time.localtime(now)
        self.file.write(
            f"{local_time.tm_year}-{local_time.tm_mon}-{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_min}:{local_time.tm_sec},{ticket_id}\n")
        self.file.flush()
