from pathlib import Path
import argparse
import os

import crypto
import config
import gui
import qr


def generate(gen_config: config.Config, progress_indicator: gui.ProgressIndicator):
    key = crypto.generate_or_get_keys(gen_config.key_dir)
    progress_indicator.set_maximum(gen_config.num_qr_codes)
    for i_code in range(gen_config.num_qr_codes):
        data = f"{gen_config.event_name}_{i_code}"
        signature = crypto.sign_message(data, key)
        qr.save_signed_message(data, signature, os.path.join(
            gen_config.out_dir, gen_config.event_name, f"{i_code}.png"))
        progress_indicator.set_progress(i_code)


if __name__ == "__main__":
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

    initial_config = config.Config(event_name, num_codes, out_dir, key_dir)

    gui.create(generate, initial_config)
