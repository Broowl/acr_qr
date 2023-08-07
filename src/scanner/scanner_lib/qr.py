import base64
import re
from types import TracebackType
from urllib.parse import unquote_to_bytes
from typing import Any, List, Optional
import cv2


def read(image: Any) -> tuple[str, Any] | None:
    detector = cv2.QRCodeDetector()
    ret_qr, decoded_info, points, _ = detector.detectAndDecodeMulti(image)
    if not ret_qr or len(decoded_info[0]) == 0:
        return None
    return (decoded_info[0], points)


def decode_message(data: str) -> tuple[str, int, bytes] | None:
    matcher = re.compile(r"^(.*)_(\d+)__(.*)$")
    matches = re.match(matcher, data)
    if matches is None:
        return None
    groups = matches.groups()
    message = groups[0]
    ticket_id = int(groups[1])
    signature = unquote_to_bytes(groups[2])
    return (message, ticket_id, base64.b64decode(signature))


class CameraCapture:
    """Class which represents camera"""

    def __init__(self) -> None:
        self.capture: Optional[cv2.VideoCapture] = None

    def __enter__(self) -> Any:
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            raise IOError("Cannot open webcam")
        return self

    def __exit__(self,
                 exc_type: type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: TracebackType | None) -> None:
        if self.capture is not None:
            self.capture.release()
            cv2.destroyAllWindows()

    def get_frame(self) -> Any:
        if self.capture is None:
            raise RuntimeError("VideoCapture not initialized")
        _, frame = self.capture.read()
        return frame

    def set_camera(self, index: int) -> None:
        if self.capture is not None:
            self.capture.release()
        self.capture = cv2.VideoCapture(index)
        if not self.capture.isOpened():
            raise IOError("Cannot open webcam")


def scan_for_cameras() -> List[int]:
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr
