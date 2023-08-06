import argparse
from typing import Any
from Crypto.PublicKey.RSA import RsaKey
from scanner_lib.display_utils import Trigger
from scanner_lib.signing import verify_message, read_key
from scanner_lib.id_storage import IdStorage
from scanner_lib.qr import decode_message, read, start_scanning


def process_frame(frame: Any, key: RsaKey, trigger: Trigger, storage: IdStorage) -> None:
    read_result = read(frame)
    if read_result is None:
        trigger.show_frame_stored(frame)
        return
    payload, frame_points = read_result
    decode_result = decode_message(payload)
    if decode_result is None:
        trigger.show_frame_denied(frame, ("Wrong format", frame_points))
        return
    message, ticket_id, signature = decode_result
    is_verified = verify_message(
        f"{message}_{ticket_id}", signature, key)
    if not is_verified:
        trigger.show_frame_denied(frame, ("Invalid signature", frame_points))
        return
    if not storage.try_add_id(ticket_id):
        trigger.show_frame_denied(frame, ("Duplicate ID", frame_points))
        return
    trigger.show_frame_verified(frame, (message, ticket_id, frame_points))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("public_key")
    parser.add_argument("id_storage_path")
    parsed_args = parser.parse_args()
    public_key_file = parsed_args.public_key
    id_storage_path = parsed_args.id_storage_path

    key = read_key(public_key_file)
    trigger = Trigger(3)
    with IdStorage(id_storage_path, 5) as id_storage:
        start_scanning(lambda arg: process_frame(
            arg, key, trigger, id_storage))


if __name__ == "__main__":
    main()
