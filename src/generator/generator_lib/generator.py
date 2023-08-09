import os
from generator_lib.signing import generate_or_get_keys, sign_message
from generator_lib.config import Config
from generator_lib.gui import ProgressIndicator
from generator_lib.qr import save_signed_message


class Generator:
    """Main class which handles generating QR-codes"""

    def __init__(self, progress_indicator: ProgressIndicator) -> None:
        self.progress_indicator = progress_indicator

    def generate(self, gen_config: Config) -> None:
        key = generate_or_get_keys(gen_config.key_dir)
        self.progress_indicator.set_maximum(gen_config.num_qr_codes)
        for i_code in range(gen_config.num_qr_codes):
            data = f"{gen_config.event_name}_{i_code}"
            signature = sign_message(data, key)
            save_signed_message(data, signature, os.path.join(
                gen_config.out_dir, gen_config.event_name, f"{i_code}.png"))
            self.progress_indicator.set_progress(i_code)