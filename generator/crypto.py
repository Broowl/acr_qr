from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import os


def save_key(key: RSA.RsaKey, file_name: str) -> None:
    file_out = open(file_name, "wb")
    file_out.write(key.export_key())
    file_out.close()


def generate_or_get_keys(file_name_private: str, file_name_public: str) -> RSA.RsaKey:
    if not os.path.exists(file_name_private):
        key = RSA.generate(2048)
        save_key(key, file_name_private)
        save_key(key.public_key(), file_name_public)
        return key
    return RSA.import_key(open(file_name_private).read())


def sign_message(message: str, private_key: RSA.RsaKey) -> bytes:
    h = SHA256.new(message.encode())
    return pss.new(private_key).sign(h)
