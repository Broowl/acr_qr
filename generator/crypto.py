import os
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256


def save_key(key: RSA.RsaKey, file_name: str) -> None:
    with open(file_name, "wb") as file_out:
        file_out.write(key.export_key())
        file_out.close()


def generate_or_get_keys(key_dir: Path) -> RSA.RsaKey:
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)
    file_name_private = str(key_dir / "private.pem")
    if not os.path.exists(file_name_private):
        key = RSA.generate(1024)
        save_key(key, file_name_private)
        file_name_public = str(key_dir / "public.pem")
        save_key(key.public_key(), file_name_public)
        return key
    with open(file_name_private, "rb") as private_key_file:
        return RSA.import_key(private_key_file.read())


def sign_message(message: str, private_key: RSA.RsaKey) -> bytes:
    hashed = SHA256.new(message.encode())
    return pss.new(private_key).sign(hashed) # type: ignore
