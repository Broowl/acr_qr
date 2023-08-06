import argparse
from typing import Any
from Crypto.PublicKey.RSA import RsaKey
from . import display_utils as du
from . import crypto
from . import id_storage as ids
from . import qr


def process_frame(frame: Any, key: RsaKey, trigger: du.Trigger, storage: ids.IdStorage) -> None:
    # pylint: disable=maybe-no-member
    read_result = qr.read(frame)
    if read_result is None:
        trigger.show_frame_stored(frame)
        return
    payload, frame_points = read_result
    decode_result = qr.decode_message(payload)
    if decode_result is None:
        trigger.show_frame_denied(frame, ("Wrong format", frame_points))
        return
    message, ticket_id, signature = decode_result
    is_verified = crypto.verify_message(
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

    key = crypto.read_key(public_key_file)
    trigger = du.Trigger(3)
    with ids.IdStorage(id_storage_path, 5) as id_storage:
        # pylint: disable=maybe-no-member
        qr.start_scanning(lambda arg: process_frame(
            arg, key, trigger, id_storage))


if __name__ == "__main__":
    main()
