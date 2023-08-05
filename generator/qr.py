import base64
import os
from urllib.parse import quote
import qrcode


def save(data: str, file_name: str) -> None:
    img = qrcode.make(data)
    if os.path.exists(file_name):
        os.remove(file_name)
    dir_name = os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    img.save(file_name)


def save_signed_message(message: str, signature: bytes, file_name: str) -> None:
    decoded_signature = quote(base64.b64encode(signature))
    data = f"{message}__{decoded_signature}"
    save(data, file_name)
