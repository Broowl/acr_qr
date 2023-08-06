from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256


def read_key(file_name: Path) -> RSA.RsaKey:
    with open(file_name, 'rb') as public_key_file:
        return RSA.import_key(public_key_file.read())


def verify_message(message: str, signature: bytes, public_key: RSA.RsaKey) -> bool:
    hashed = SHA256.new(message.encode())
    verifier = pss.new(public_key)
    try:
        verifier.verify(hashed, signature)
        return True
    except (ValueError, TypeError):
        return False
