import base64
from typing import Any, Callable
import cv2
from urllib.parse import unquote_to_bytes
import re


def read(image) -> tuple[str, Any] | None:
    detector = cv2.QRCodeDetector()
    try:
        ret_qr, decoded_info, points, _ = detector.detectAndDecodeMulti(image)
        if not ret_qr or len(decoded_info[0]) == 0:
            return None
        return (decoded_info[0], points)
    except:
        return None


def decode_message(data: str) -> tuple[str, bytes]:
    matcher = re.compile(r"^(.*)__(.*)$")
    matches = re.match(matcher, data).groups()
    message = matches[0]
    signature = unquote_to_bytes(matches[1])
    return (message, base64.b64decode(signature))


def process_frame(frame, callback: Callable[[str, bytes], None]) -> None:
    data = read(frame)
    if data is None:
        cv2.imshow('camera', frame)
        return
    frame_with_border = cv2.polylines(frame, [data[1].astype(int)], True, (0, 255, 0), 8)
    cv2.imshow('camera', frame_with_border)
    callback(decode_message(data[0]))


def start_scanning(callback: Callable[[str, bytes], None]) -> None:
    cap = cv2.VideoCapture(1)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()

        c = cv2.waitKey(1)
        if c == 27:
            break
        if ret is True:
            process_frame(frame, callback)

    cap.release()
    cv2.destroyAllWindows()
