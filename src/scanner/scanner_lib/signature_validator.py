import os
from pathlib import Path
from typing import Optional
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from .persistence import Persistence


class SignatureValidator:
    """Class which verifies signatures"""

    def __init__(self, file_name: Path, persistence: Persistence) -> None:
        self.key: Optional[RSA.RsaKey] = read_key(file_name)
        self.persistence = persistence

    def set_key(self, file_name: Path) -> None:
        self.key = read_key(file_name)
        self.persistence.persist_key_path(file_name)

    def verify_message(self, message: str, signature: bytes) -> bool:
        if self.key is None:
            return False
        hashed = SHA256.new(message.encode())
        verifier = pss.new(self.key)
        try:
            verifier.verify(hashed, signature)
            return True
        except (ValueError, TypeError):
            return False


def read_key(file_name: Path) -> Optional[RSA.RsaKey]:
    if not os.path.exists(file_name):
        return None
    with open(file_name, 'rb') as public_key_file:
        return RSA.import_key(public_key_file.read())
