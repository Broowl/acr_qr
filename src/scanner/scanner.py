import argparse
from pathlib import Path
from typing import Any
from Crypto.PublicKey.RSA import RsaKey
from scanner_lib.display_utils import Trigger
from scanner_lib.signing import verify_message, read_key
from scanner_lib.id_storage import IdStorage
from scanner_lib.qr import decode_message, read, CameraCapture
from scanner_lib.gui import create, FramePainter
from scanner_lib.config import Config


def process_frame(camera_capture: CameraCapture, key: RsaKey, trigger: Trigger, storage: IdStorage, painter: FramePainter) -> None:
    frame = camera_capture.get_frame()
    read_result = read(frame)
    if read_result is None:
        trigger.show_frame_stored(frame, painter)
        return
    payload, frame_points = read_result
    decode_result = decode_message(payload)
    if decode_result is None:
        trigger.show_frame_denied(
            frame, ("Wrong format", frame_points), painter)
        return
    message, ticket_id, signature = decode_result
    is_verified = verify_message(
        f"{message}_{ticket_id}", signature, key)
    if not is_verified:
        trigger.show_frame_denied(
            frame, ("Invalid signature", frame_points), painter)
        return
    if not storage.try_add_id(ticket_id):
        trigger.show_frame_denied(
            frame, ("Duplicate ID", frame_points), painter)
        return
    trigger.show_frame_verified(
        frame, (message, ticket_id, frame_points), painter)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--public_key")
    parser.add_argument("-l", "--log_dir")
    parsed_args = parser.parse_args()

    default_dir = Path.home() / "Documents" / "ACR_QR_Scanner"
    log_dir = default_dir / "Logs"
    public_key_path = default_dir / "Keys" / "public.pem"

    if parsed_args.log_dir is not None:
        log_dir = Path(parsed_args.log_dir)
    if parsed_args.public_key is not None:
        public_key_path = Path(parsed_args.public_key)

    initial_config = Config(log_dir, public_key_path)
    key = read_key(public_key_path)
    trigger = Trigger(3)

    with IdStorage(log_dir, 5) as id_storage:
        with CameraCapture() as camera_capture:
            create(lambda painter: process_frame(camera_capture, key,
                   trigger, id_storage, painter), initial_config)


if __name__ == "__main__":
    main()
