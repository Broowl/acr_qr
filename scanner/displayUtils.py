import time
from typing import Any
import cv2
import numpy as np


class Trigger:
    def __init__(self, trigger_length: float) -> None:
        self.timer = None
        self.trigger_length = trigger_length

    def show_frame(self, frame: Any, args: tuple[Any, Any] | None = None) -> None:
        if args is None:
            self._show_frame_stored(frame)
            return
        self._show_frame_new(frame, args)

    def _show_frame_new(self, frame: Any, args: tuple[Any, Any]) -> None:
        self._trigger()
        self.args = args
        show_frame(decorate_frame_green(frame, args[0], args[1]))

    def _show_frame_stored(self, frame: Any) -> None:
        if self._get_is_triggered():
            show_frame(decorate_frame_green(frame, self.args[0], self.args[1]))
            return
        show_frame(frame)

    def _trigger(self) -> None:
        self.timer = time.time()

    def _get_is_triggered(self) -> bool:
        if self.timer is None:
            return False
        return time.time() - self.timer < self.trigger_length


def show_frame(frame) -> None:
    cv2.imshow('camera', frame)


def decorate_frame_green(frame, text: str, points):
    font = cv2.FONT_HERSHEY_SIMPLEX
    int_points = [points.astype(int)]
    org = np.copy(int_points[0][0][0])
    org[0] += 10
    org[1] += 30
    fontScale = 1
    color = (20, 220, 15)
    thickness = 2
    cv2.LINE_AA
    decorated = cv2.putText(frame, text, org, font,
                            fontScale, (255, 255, 255), thickness * 4, cv2.LINE_AA)
    decorated = cv2.putText(decorated, text, org, font,
                            fontScale, color, thickness, cv2.LINE_AA)
    decorated = cv2.polylines(decorated, int_points, True, color, 8)
    return decorated
