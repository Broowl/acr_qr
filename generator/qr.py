import base64
import qrcode
import os
from urllib.parse import quote


def save(data: str, file_name: str) -> None:
    img = qrcode.make(data)
    if os.path.exists(file_name):
        os.remove(file_name)
    img.save(file_name)


def save_signed_message(message: str, signature: bytes, file_name: str) -> None:
    decoded_signature = quote(base64.b64encode(signature)) 
    data = f"{message}__{decoded_signature}"
    save(data, file_name)
