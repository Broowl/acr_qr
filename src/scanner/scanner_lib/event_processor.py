from pathlib import Path
import queue
from enum import Enum
import threading
from typing import Callable, Dict, Optional


class EventType(Enum):
    """Event types"""
    PROCESS_FRAME = 1
    SET_KEY_PATH = 2
    SET_LOG_DIR = 3
    SET_CAMERA = 4


class Event:
    """Base class for events"""

    def __init__(self, event_type: EventType) -> None:
        self.event_type = event_type

    def get_event_type(self) -> EventType:
        return self.event_type


class ProcessFrameEvent(Event):
    """Event signaling frame processing"""

    def __init__(self) -> None:
        super().__init__(EventType.PROCESS_FRAME)


ProcessFrameEventHandler = Callable[[ProcessFrameEvent], None]


class SetKeyPathEvent(Event):
    """Event singnaling a key path change"""

    def __init__(self, key_path: Path) -> None:
        super().__init__(EventType.SET_KEY_PATH)
        self.key_path = key_path


SetKeyPathEventHandler = Callable[[SetKeyPathEvent], None]


class SetLogDirEvent(Event):
    """Event signaling a log directory change"""

    def __init__(self, log_dir: Path) -> None:
        super().__init__(EventType.SET_LOG_DIR)
        self.log_dir = log_dir


SetLogDirEventHandler = Callable[[SetLogDirEvent], None]


class SetCameraEvent(Event):
    """Event signaling a camera change"""

    def __init__(self, camera_index: int) -> None:
        super().__init__(EventType.SET_CAMERA)
        self.camera_index = camera_index


SetCameraEventHandler = Callable[[SetCameraEvent], None]

EventHandler = ProcessFrameEventHandler | SetKeyPathEventHandler | SetLogDirEventHandler | SetCameraEventHandler


class EventProcessor:
    """Event processor which dispatches GUI events"""

    def __init__(self) -> None:
        self.event_queue: queue.Queue[Event] = queue.Queue()
        self.processors: Dict[EventType, EventHandler] = {}
        self.processor_thread: Optional[threading.Thread] = None
        self.stop_requested = False

    def register_processor(self, event_type: EventType, handler: EventHandler) -> None:
        self.processors[event_type] = handler

    def push(self, event: Event) -> None:
        self.event_queue.put(event)

    def start(self) -> None:
        self.processor_thread = threading.Thread(target=self._process, args=())
        self.processor_thread.start()

    def _process(self) -> None:
        while (not self.stop_requested):
            event = self.event_queue.get()
            event_type = event.get_event_type()
            processor = self.processors.get(event_type)
            if processor is not None:
                processor(event)  # type: ignore[arg-type]

    def stop(self) -> None:
        self.stop_requested = True
        if self.processor_thread is not None:
            self.processor_thread.join()
