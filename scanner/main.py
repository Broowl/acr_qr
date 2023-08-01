import displayUtils as du
import crypto
import qr
import argparse
from Crypto.PublicKey.RSA import RsaKey
import idStorage as ids


def process_frame(frame, key: RsaKey, trigger: du.Trigger, storage: ids.IdStorage) -> None:
    readResult = qr.read(frame)
    if readResult is None:
        trigger.show_frame_stored(frame)
        return
    payload, frame_points = readResult
    decodeResult = qr.decode_message(payload)
    if decodeResult is None:
        trigger.show_frame_denied(frame, ("Wrong format", frame_points))
        return
    message, id, signature = decodeResult
    is_verified = crypto.verify_message(f"{message}_{id}", signature, key)
    if not is_verified:
        trigger.show_frame_denied(frame, ("Invalid signature", frame_points))
        return
    if not storage.try_add_id(id):
        trigger.show_frame_denied(frame, ("Duplicate ID", frame_points))
        return
    trigger.show_frame_verified(frame, (message, id, frame_points))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("public_key")
    parser.add_argument("id_storage_path")
    parsed_args = parser.parse_args()
    public_key_file = parsed_args.public_key
    id_storage_path = parsed_args.id_storage_path

    key = crypto.read_key(public_key_file)
    trigger = du.Trigger(3)
    with ids.IdStorage(id_storage_path, 5) as idStorage:
        qr.start_scanning(lambda arg: process_frame(arg, key, trigger, idStorage))
