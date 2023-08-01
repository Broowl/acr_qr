import displayUtils as du
import crypto
import qr
import argparse
from Crypto.PublicKey.RSA import RsaKey


def process_frame(frame, key: RsaKey, trigger: du.Trigger) -> None:
    data = qr.read(frame)
    if data is None:
        trigger.show_frame(frame)
        return
    decoded = qr.decode_message(data[0])
    if decoded is None:
        trigger.show_frame(frame)
        return
    is_verified = crypto.verify_message(decoded[0], decoded[1], key)
    if not is_verified:
        trigger.show_frame(frame)
        return
    trigger.show_frame(frame, (decoded[0], data[1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("public_key")
    parsed_args = parser.parse_args()
    public_key_file = parsed_args.public_key

    key = crypto.read_key(public_key_file)
    trigger = du.Trigger(3)
    qr.start_scanning(lambda arg: process_frame(arg, key, trigger))
