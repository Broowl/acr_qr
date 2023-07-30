from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def generate():
    return RSA.generate(2048)


def sign_message(message : str, private_key: RSA.RsaKey) -> bytes:
    h = SHA256.new(message.encode())
    return pss.new(private_key).sign(h)


def verify_message(message:str, signature: bytes, public_key: RSA.RsaKey) -> bool:
    h = SHA256.new(message.encode())
    verifier = pss.new(public_key)
    try:
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False