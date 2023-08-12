from pathlib import Path
import queue
from enum import Enum
import threading
from typing import Callable, Generic, List, Optional, TypeVar


class EventType(Enum):
    """Event types"""
    PROCESS_FRAME = 1
    SET_KEY_PATH = 2
    SET_LOG_DIR = 3
    SET_CAMERA = 4
    SET_EVENT_NAME = 5


class Event:
    """Base class for events"""

    def __init__(self, event_type: EventType) -> None:
        self.event_type = event_type

    def get_event_type(self) -> EventType:
        return self.event_type


EventT = TypeVar('EventT', bound=Event)


class EventHandler(Generic[EventT]):
    """Generic event handler type"""

    def __init__(self, handler: Callable[[EventT], None], handled_type: EventType) -> None:
        self.handler = handler
        self.handled_type = handled_type

    def call(self, event: Event) -> None:
        if event.get_event_type() == self.handled_type:
            self.handler(event)  # type: ignore[arg-type]


class ProcessFrameEvent(Event):
    """Event signaling frame processing"""

    def __init__(self, origin_time: float) -> None:
        super().__init__(EventType.PROCESS_FRAME)
        self.origin_time = origin_time


class ProcessFrameEventHandler(EventHandler[ProcessFrameEvent]):
    """ProcessFrameEventHandler"""

    def __init__(self, handler: Callable[[ProcessFrameEvent], None]) -> None:
        super().__init__(handler, EventType.PROCESS_FRAME)


class SetKeyPathEvent(Event):
    """Event singnaling a key path change"""

    def __init__(self, key_path: Path) -> None:
        super().__init__(EventType.SET_KEY_PATH)
        self.key_path = key_path


class SetKeyPathEventHandler(EventHandler[SetKeyPathEvent]):
    """SetKeyPathEventHandler"""

    def __init__(self, handler: Callable[[SetKeyPathEvent], None]) -> None:
        super().__init__(handler, EventType.SET_KEY_PATH)


class SetLogDirEvent(Event):
    """Event signaling a log directory change"""

    def __init__(self, log_dir: Path) -> None:
        super().__init__(EventType.SET_LOG_DIR)
        self.log_dir = log_dir


class SetLogDirEventHandler(EventHandler[SetLogDirEvent]):
    """SetLogDirEventHandler"""

    def __init__(self, handler: Callable[[SetLogDirEvent], None]) -> None:
        super().__init__(handler, EventType.SET_LOG_DIR)


class SetCameraEvent(Event):
    """Event signaling a camera change"""

    def __init__(self, camera_index: int) -> None:
        super().__init__(EventType.SET_CAMERA)
        self.camera_index = camera_index


class SetCameraEventHandler(EventHandler[SetCameraEvent]):
    """SetCameraEventHandler"""

    def __init__(self, handler: Callable[[SetCameraEvent], None]) -> None:
        super().__init__(handler, EventType.SET_CAMERA)

class SetEventNameEvent(Event):
    """Event signaling an event name change"""

    def __init__(self, event_name: str) -> None:
        super().__init__(EventType.SET_EVENT_NAME)
        self.event_name = event_name


class SetEventNameEventHandler(EventHandler[SetEventNameEvent]):
    """SetEventNameEventHandler"""

    def __init__(self, handler: Callable[[SetEventNameEvent], None]) -> None:
        super().__init__(handler, EventType.SET_EVENT_NAME)


EventHandlers = ProcessFrameEventHandler | \
    SetKeyPathEventHandler | \
    SetLogDirEventHandler | \
    SetCameraEventHandler | \
    SetEventNameEventHandler


class EventProcessor:
    """Event processor which dispatches GUI events"""

    def __init__(self) -> None:
        self.event_queue: queue.Queue[Event] = queue.Queue()
        self.processors: List[EventHandlers] = []
        self.processor_thread: Optional[threading.Thread] = None
        self.stop_requested = False

    def register_processor(self, handler: EventHandlers) -> None:
        self.processors.append(handler)

    def push(self, event: Event) -> None:
        self.event_queue.put(event)

    def start(self) -> None:
        self.processor_thread = threading.Thread(target=self._process, args=())
        self.processor_thread.start()

    def _process(self) -> None:
        while not self.stop_requested:
            event = self.event_queue.get()
            for processor in self.processors:
                processor.call(event)

    def stop(self) -> None:
        self.stop_requested = True
        if self.processor_thread is not None:
            self.processor_thread.join()
