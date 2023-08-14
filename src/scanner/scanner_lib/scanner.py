import time
from typing import Optional
from scanner_lib.signature_validator import SignatureValidator
from scanner_lib.display_utils import QrCodeImageDrawer
from scanner_lib.id_storage import IdStorage
from scanner_lib.qr import decode_message, read, CameraCapture
from scanner_lib.event_characteristics import EventCharacteristics


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
        self.event_characteristics: Optional[EventCharacteristics] = None

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
        if self.event_characteristics is not None and decode_result.event_name != self.event_characteristics.name:
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Wrong event name", frame_points))
            return
        if self.event_characteristics is not None and decode_result.event_date != self.event_characteristics.date:
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Wrong event date", frame_points))
            return
        is_verified = self.validator.verify_message(
            decode_result.encoded, decode_result.signature)
        if not is_verified:
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Invalid signature", frame_points))
            return
        if not self.storage.try_add_id(decode_result.ticket_id):
            self.qr_code_image_drawer.show_frame_denied(
                frame, ("Duplicate ID", frame_points))
            return
        self.qr_code_image_drawer.show_frame_verified(
            frame, (decode_result.event_name, decode_result.ticket_id, frame_points))

    def set_event_characteristics(self, event_characteristics: EventCharacteristics) -> None:
        self.event_characteristics = event_characteristics
