import base64
import re
from urllib.parse import unquote_to_bytes
from typing import Any, Callable
import cv2


def read(image) -> tuple[str, Any] | None:
    detector = cv2.QRCodeDetector()
    ret_qr, decoded_info, points, _ = detector.detectAndDecodeMulti(image)
    if not ret_qr or len(decoded_info[0]) == 0:
        return None
    return (decoded_info[0], points)


def decode_message(data: str) -> tuple[str, bytes] | None:
    matcher = re.compile(r"^(.*)_(\d+)__(.*)$")
    matches = re.match(matcher, data)
    if matches is None:
        return None
    groups = matches.groups()
    message = groups[0]
    ticket_id = int(groups[1])
    signature = unquote_to_bytes(groups[2])
    return (message, ticket_id, base64.b64decode(signature))


def start_scanning(callback: Callable[[Any], None]) -> None:
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()

        c = cv2.waitKey(1)
        if c == 27:
            break
        if ret is True:
            callback(frame)

    cap.release()
    cv2.destroyAllWindows()
