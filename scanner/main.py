import crypto
import qr
import argparse
import os
from Crypto.PublicKey.RSA import RsaKey
import cv2


def print_verification(arg: tuple[str, bytes] | None, key: RsaKey) -> None:
    if arg is None:
        return
    is_verified = crypto.verify_message(arg[0], arg[1], key)
    if is_verified:
        print("Access granted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("public_key")
    parsed_args = parser.parse_args()
    public_key_file = parsed_args.public_key

    key = crypto.read_key(public_key_file)
    qr.start_scanning(lambda arg: print_verification(arg, key))
