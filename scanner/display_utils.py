import time
from typing import Any
import cv2
import numpy as np


class Trigger:
    """Class for displaying smooth frames around detected QR-codes"""
    def __init__(self, trigger_length: float) -> None:
        self.timer = None
        self.trigger_length = trigger_length
        self.args = None

    def show_frame_verified(self, frame: Any, args: tuple[str, int, Any]) -> None:
        self._trigger()
        self.args = args
        show_frame(decorate_frame_green(frame, args[0], args[1], args[2]))

    def show_frame_denied(self, frame: Any, args: tuple[str, Any]) -> None:
        self._trigger()
        self.args = args
        show_frame(decorate_frame_red(frame, args[0], args[1]))

    def show_frame_stored(self, frame: Any) -> None:
        if self._get_is_triggered():
            self._show_frame_stored(frame)
            return
        show_frame(frame)

    def _trigger(self) -> None:
        self.timer = time.time()

    def _get_is_triggered(self) -> bool:
        if self.timer is None:
            return False
        return time.time() - self.timer < self.trigger_length

    def _show_frame_stored(self, frame):
        if self.args is None:
            return
        if len(self.args) == 3:
            show_frame(decorate_frame_green(
                frame, self.args[0], self.args[1], self.args[2]))
        else:
            show_frame(decorate_frame_red(
                frame, self.args[0], self.args[1]))


def show_frame(frame) -> None:
    cv2.imshow('camera', frame)


def decorate_frame_green(frame, event: str, ticket_id: int, points):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    int_points = [points.astype(int)]
    color = (20, 220, 15)
    thickness = 2

    first_line = f"Event: {event}"
    first_line_origin = np.copy(int_points[0][0][0])
    first_line_origin[0] += 10  # horizontal offset
    first_line_origin[1] += 40  # vertical offset

    decorated = cv2.putText(frame, first_line, first_line_origin, font,
                            font_scale, (255, 255, 255), thickness * 4, cv2.LINE_AA)
    decorated = cv2.putText(decorated, first_line, first_line_origin, font,
                            font_scale, color, thickness, cv2.LINE_AA)
    second_line = f"ID: {ticket_id}"
    second_line_origin = np.copy(int_points[0][0][0])
    second_line_origin[0] += 10  # horizontal offset
    second_line_origin[1] += 100  # vertical offset
    decorated = cv2.putText(decorated, second_line, second_line_origin, font,
                            font_scale, (255, 255, 255), thickness * 4, cv2.LINE_AA)
    decorated = cv2.putText(decorated, second_line, second_line_origin, font,
                            font_scale, color, thickness, cv2.LINE_AA)
    decorated = cv2.polylines(decorated, int_points, True, color, 8)
    return decorated


def decorate_frame_red(frame, reason: str, points):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    int_points = [points.astype(int)]
    color = (10, 10, 230)
    thickness = 2

    first_line = reason
    first_line_origin = np.copy(int_points[0][0][0])
    first_line_origin[0] += 10  # horizontal offset
    first_line_origin[1] += 40  # vertical offset

    decorated = cv2.putText(frame, first_line, first_line_origin, font,
                            font_scale, (255, 255, 255), thickness * 4, cv2.LINE_AA)
    decorated = cv2.putText(decorated, first_line, first_line_origin, font,
                            font_scale, color, thickness, cv2.LINE_AA)
    decorated = cv2.polylines(decorated, int_points, True, color, 8)
    return decorated
