import base64
import qrcode
import cv2
import os
from urllib.parse import unquote_to_bytes
import re
from qreader import QReader


def read(file_name: str) -> str:
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)
    return decoded_text[0]


def read_signed_message(file_name: str) -> tuple[str, bytes]:
    data = read(file_name)
    matcher = re.compile(r"^(.*)__(.*)$")
    matches = re.match(matcher, data).groups()
    message = matches[0]
    signature = unquote_to_bytes(matches[1])
    return (message, base64.b64decode(signature))
