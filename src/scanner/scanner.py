import argparse
from pathlib import Path
import time
from typing import cast
from scanner_lib.persistence import Persistence, PersistedValues
from scanner_lib.signature_validator import SignatureValidator
from scanner_lib.display_utils import QrCodeImageDrawer
from scanner_lib.id_storage import IdStorage
from scanner_lib.qr import decode_message, read, CameraCapture, scan_for_cameras
from scanner_lib.gui import ScannerGui
from scanner_lib.config import Config
from scanner_lib.event_processor import EventProcessor,\
    ProcessFrameEvent, ProcessFrameEventHandler, \
    SetKeyPathEvent, SetKeyPathEventHandler, \
    SetLogDirEvent, SetLogDirEventHandler,\
    SetCameraEvent, SetCameraEventHandler


class Scanner:
    """Main class which handles scanning of QR codes"""

    def __init__(self, camera_capture: CameraCapture,
                 validator: SignatureValidator,
                 qr_code_image_drawer: QrCodeImageDrawer,
                 storage: IdStorage) -> None:
        self.camera_capture = camera_capture
        self.validator = validator
        self.qr_code_image_drawer = qr_code_image_drawer
        self.storage = storage

    def process_frame(self, origin_time: float) -> None:
        if time.time() - origin_time > 1:
            return
        frame = self.camera_capture.get_frame()
        read_result = read(frame)
        if read_result is None:
            self.qr_code_image_drawer.show_frame_stored(frame)
            return
        payload, frame_points = read_result
        decode_result = decode_message(payload)
        if decode_result is None:
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Wrong format", frame_points))
            return
        message, ticket_id, signature = decode_result
        is_verified = self.validator.verify_message(
            f"{message}_{ticket_id}", signature)
        if not is_verified:
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Invalid signature", frame_points))
            return
        if not self.storage.try_add_id(ticket_id):
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Duplicate ID", frame_points))
            return
        self.qr_code_image_drawer.show_frame_verified(
            frame, (message, ticket_id, frame_points))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--public_key")
    parser.add_argument("-l", "--log_dir")
    parsed_args = parser.parse_args()

    default_dir = Path.home() / "Documents" / "ACR_QR_Scanner"
    log_dir = default_dir / "Logs"
    public_key_path = default_dir / "Keys" / "public.pem"
    config_path = default_dir / "config.json"
    camera_index = 0

    persistence = Persistence(config_path, PersistedValues(
        log_dir, public_key_path, camera_index))
    log_dir = persistence.get_persisted_log_dir()
    public_key_path = persistence.get_persisted_key_path()
    camera_index = persistence.get_persisted_camera_index()

    if parsed_args.log_dir is not None:
        log_dir = Path(parsed_args.log_dir)
        persistence.persist_log_dir(log_dir)
    if parsed_args.public_key is not None:
        public_key_path = Path(parsed_args.public_key)
        persistence.persist_key_path(public_key_path)

    initial_config = Config(log_dir, public_key_path)
    validator = SignatureValidator(public_key_path, persistence)

    gui = ScannerGui(initial_config, scan_for_cameras())
    painter = gui.get_painter()
    qr_code_image_drawer = QrCodeImageDrawer(3, painter)
    with IdStorage(log_dir, 5, persistence) as id_storage_any:
        id_storage = cast(IdStorage, id_storage_any)
        with CameraCapture(camera_index, persistence) as camera_capture_any:
            camera_capture = cast(CameraCapture, camera_capture_any)
            scanner = Scanner(camera_capture, validator,
                              qr_code_image_drawer, id_storage)
            event_processor = EventProcessor()

            event_processor.register_processor(
                ProcessFrameEventHandler(lambda event: scanner.process_frame(event.origin_time)))
            event_processor.register_processor(
                SetKeyPathEventHandler(lambda event: validator.set_key(event.key_path)))
            event_processor.register_processor(
                SetLogDirEventHandler(lambda event: id_storage.set_dir(event.log_dir)))
            event_processor.register_processor(
                SetCameraEventHandler(lambda event: camera_capture.set_camera(event.camera_index)))

            gui.set_timer_listener(
                lambda: event_processor.push(ProcessFrameEvent(time.time())))
            gui.set_key_path_changed_listener(
                lambda key_path: event_processor.push(SetKeyPathEvent(key_path)))
            gui.set_log_dir_changed_listener(
                lambda log_dir: event_processor.push(SetLogDirEvent(log_dir)))
            gui.set_camera_listener(
                lambda camera_index: event_processor.push(SetCameraEvent(camera_index)))

            event_processor.start()
            gui.run()
            event_processor.stop()


if __name__ == "__main__":
    main()
