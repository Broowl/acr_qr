import argparse
from pathlib import Path
from typing import cast
from scanner_lib.signature_validator import SignatureValidator
from scanner_lib.display_utils import QrCodeImageDrawer
from scanner_lib.id_storage import IdStorage
from scanner_lib.qr import decode_message, read, CameraCapture
from scanner_lib.gui import ScannerGui
from scanner_lib.config import Config


class Scanner:
    """Main class which handles scanning of QR codes"""
    def __init__(self, camera_capture: CameraCapture,
                 validator: SignatureValidator,
                 trigger: QrCodeImageDrawer,
                 storage: IdStorage) -> None:
        self.camera_capture = camera_capture
        self.validator = validator
        self.trigger = trigger
        self.storage = storage

    def process_frame(self) -> None:
        frame = self.camera_capture.get_frame()
        read_result = read(frame)
        if read_result is None:
            self.trigger.show_frame_stored(frame)
            return
        payload, frame_points = read_result
        decode_result = decode_message(payload)
        if decode_result is None:
            self.trigger.show_frame_denied(
                frame, ("Wrong format", frame_points))
            return
        message, ticket_id, signature = decode_result
        is_verified = self.validator.verify_message(
            f"{message}_{ticket_id}", signature)
        if not is_verified:
            self.trigger.show_frame_denied(
                frame, ("Invalid signature", frame_points))
            return
        if not self.storage.try_add_id(ticket_id):
            self.trigger.show_frame_denied(
                frame, ("Duplicate ID", frame_points))
            return
        self.trigger.show_frame_verified(
            frame, (message, ticket_id, frame_points))


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
    validator = SignatureValidator(public_key_path)

    gui = ScannerGui(initial_config)
    painter = gui.get_painter()
    trigger = QrCodeImageDrawer(3, painter)
    with IdStorage(log_dir, 5) as id_storage_any:
        id_storage = cast(IdStorage, id_storage_any)
        with CameraCapture() as camera_capture:
            scanner = Scanner(camera_capture, validator, trigger, id_storage)
            gui.set_timer_listener(scanner.process_frame)
            gui.set_key_path_changed_listener(validator.set_key)
            gui.set_log_dir_changed_listener(id_storage.set_dir)
            gui.run()


if __name__ == "__main__":
    main()
