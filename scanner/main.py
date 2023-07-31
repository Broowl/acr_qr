import crypto
import qr
import argparse
from Crypto.PublicKey.RSA import RsaKey
import cv2
import numpy as np

def show_frame(frame) -> None:
    cv2.imshow('camera', frame)

def decorate_frame(frame, text:str, points):
    font = cv2.FONT_HERSHEY_SIMPLEX
    int_points = [points.astype(int)]
    org = np.copy(int_points[0][0][0])
    org[0] += 10
    org[1] += 30
    fontScale = 1
    color = (0, 255, 0)
    thickness = 2
    decorated = cv2.putText(frame, text, org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    decorated = cv2.polylines(decorated, int_points, True, color, 8)
    return decorated

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
    show_frame(decorate_frame(frame, decoded[0], data[1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("public_key")
    parsed_args = parser.parse_args()
    public_key_file = parsed_args.public_key

    key = crypto.read_key(public_key_file)
    qr.start_scanning(lambda arg: process_frame(arg, key))
