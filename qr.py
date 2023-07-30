import base64
import qrcode
import cv2
import os
from urllib.parse import quote, unquote_to_bytes
import re
from qreader import QReader


def save(data: str, file_name: str) -> None:
    img = qrcode.make(data)
    if os.path.exists(file_name):
        os.remove(file_name)
    img.save(file_name)


def save_signed_message(message: str, signature: bytes, file_name: str) -> None:
    decoded_signature = quote(base64.b64encode(signature)) 
    data = f"{message}__{decoded_signature}"
    save(data, file_name)


def read(file_name: str) -> str:
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)
    return decoded_text[0]

def read_signed_message(file_name:str) ->tuple[str,bytes]:
    data = read(file_name)
    matcher = re.compile(r"^(.*)__(.*)$")
    matches = re.match(matcher, data).groups()
    message = matches[0]
    signature = unquote_to_bytes(matches[1])
    return (message, base64.b64decode(signature))
