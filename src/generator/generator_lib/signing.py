import os
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256


def save_key(key: RSA.RsaKey, file_name: str) -> None:
    with open(file_name, "wb") as file_out:
        file_out.write(key.export_key())
        file_out.close()


def read_key(private_key_path: Path) -> RSA.RsaKey:
    if not os.path.exists(private_key_path):
        write_keys(private_key_path)
    with open(private_key_path, "rb") as private_key_file:
        return RSA.import_key(private_key_file.read())


def write_keys(private_key_path: Path) -> None:
    if not os.path.exists(private_key_path.parent):
        os.makedirs(private_key_path.parent)
    key = RSA.generate(1024)
    save_key(key, str(private_key_path))
    file_name_public = str(private_key_path.parent / "public.pem")
    save_key(key.public_key(), file_name_public)


def sign_message(message: str, private_key: RSA.RsaKey) -> bytes:
    hashed = SHA256.new(message.encode())
    return pss.new(private_key).sign(hashed)
