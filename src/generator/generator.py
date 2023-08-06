from pathlib import Path
import argparse
import os

from generator_lib.signing import generate_or_get_keys, sign_message
from generator_lib.config import Config
from generator_lib.gui import GeneratorGui, ProgressIndicator
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out_dir")
    parser.add_argument("-k", "--key_dir")
    parser.add_argument("-n", "--num_codes")
    parser.add_argument("-e", "--event_name")
    parsed_args = parser.parse_args()

    default_dir = Path.home() / "Documents" / "ACR_QR_Generator"
    out_dir = default_dir / "Codes"
    key_dir = default_dir / "Keys"
    event_name: str = ""
    num_codes: int = 100
    if parsed_args.out_dir is not None:
        out_dir = Path(parsed_args.out_dir)
    if parsed_args.key_dir is not None:
        key_dir = Path(parsed_args.key_dir)
    if parsed_args.event_name is not None:
        event_name = parsed_args.event_name
    if parsed_args.num_codes is not None:
        num_codes = parsed_args.num_codes

    initial_config = Config(event_name, num_codes, out_dir, key_dir)

    gui = GeneratorGui(initial_config)
    progress_indicator = gui.get_progress_indicator()
    generator = Generator(progress_indicator)
    gui.set_generator(generator.generate)
    gui.run()


if __name__ == "__main__":
    main()
