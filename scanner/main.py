import crypto
import qr
import argparse
from Crypto.PublicKey.RSA import RsaKey
import cv2


def show_frame(frame) -> None:
    cv2.imshow('camera', frame)


def process_frame(frame, key: RsaKey) -> None:
    data = qr.read(frame)
    if data is None:
        show_frame(frame)
        return
    decoded = qr.decode_message(data[0])
    if decoded is None:
        show_frame(frame)
        return
    is_verified = crypto.verify_message(decoded[0], decoded[1], key)
    if not is_verified:
        show_frame(frame)
        return
    show_frame(cv2.polylines(
            frame, [data[1].astype(int)], True, (0, 255, 0), 8))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("public_key")
    parsed_args = parser.parse_args()
    public_key_file = parsed_args.public_key

    key = crypto.read_key(public_key_file)
    qr.start_scanning(lambda arg: process_frame(arg, key))
