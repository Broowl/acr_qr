import os
import threading
from typing import Optional
from generator_lib.signing import read_key, sign_message
from generator_lib.config import Config
from generator_lib.gui import ProgressIndicator
from generator_lib.qr import TicketWriter, add_signature_to_message


class Generator:
    """Main class which handles generating QR-codes"""

    def __init__(self, progress_indicator: ProgressIndicator) -> None:
        self.progress_indicator = progress_indicator
        self.processor_thread: Optional[threading.Thread] = None

    def _generate(self, gen_config: Config) -> None:
        key = read_key(gen_config.private_key_path)
        self.progress_indicator.set_maximum(gen_config.num_qr_codes)
        writer = TicketWriter(gen_config.flyer_file_name)
        for i_code in range(gen_config.num_qr_codes):
            data = f"{gen_config.event_name}_{gen_config.event_date.strftime('%Y-%m-%d')}_{i_code}"
            signature = sign_message(data, key)
            folder_name = f"{gen_config.event_date.strftime('%Y-%m-%d')}_{gen_config.event_name}"
            file_name = f"{folder_name}_{i_code}"
            file_path = os.path.join(
                gen_config.out_dir, folder_name, file_name)
            signed = add_signature_to_message(data, signature)
            writer.save_ticket(signed, file_path)
            self.progress_indicator.set_progress(i_code)
        self.processor_thread = None

    def generate(self, gen_config: Config) -> None:
        if self.processor_thread is None:
            self.processor_thread = threading.Thread(
                target=self._generate, args=[gen_config])
            self.processor_thread.start()
