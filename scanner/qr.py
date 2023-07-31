import base64
from typing import Callable
import cv2
from urllib.parse import unquote_to_bytes
import re
from qreader import QReader


def read(image) -> str | None:
    qreader = QReader()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)
    if (decoded_text is None) or (len(decoded_text) == 0) or (decoded_text[0] is None):
        return None
    return decoded_text[0]


def read_signed_message(image) -> tuple[str, bytes] | None:
    data = read(image)
    if (data is None):
        return None
    matcher = re.compile(r"^(.*)__(.*)$")
    matches = re.match(matcher, data).groups()
    message = matches[0]
    signature = unquote_to_bytes(matches[1])
    return (message, base64.b64decode(signature))


def start_scanning(callback: Callable[[str, bytes], None]) -> None:
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break
        callback(read_signed_message(frame))

    cap.release()
    cv2.destroyAllWindows()
