from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def read_key(file_name:str)-> RSA.RsaKey:
    return RSA.import_key(open(file_name).read())

def verify_message(message:str, signature: bytes, public_key: RSA.RsaKey) -> bool:
    h = SHA256.new(message.encode())
    verifier = pss.new(public_key)
    try:
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False