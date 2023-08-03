import crypto
import qr
import argparse
import os
import gui


def generate(event_name: str,
             num_codes: int,
             out_dir: str,
             private_key_file: str,
             public_key_file: str,
             progress_indicator: gui.ProgressIndicator):
    key = crypto.generate_or_get_keys(private_key_file, public_key_file)
    for i_code in range(num_codes):
        data = f"{event_name}_{i_code}"
        signature = crypto.sign_message(data, key)
        qr.save_signed_message(data, signature, os.path.join(
            out_dir, event_name, f"{i_code}.png"))
        progress_indicator.set_progress(i_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("out_dir")
    parser.add_argument("-puk", "--public_key")
    parser.add_argument("-prk", "--private_key")
    parsed_args = parser.parse_args()
    out_dir = parsed_args.out_dir
    public_key_file = parsed_args.public_key
    private_key_file = parsed_args.private_key

    gui.create(lambda event_name, num_codes, progress_indicator: generate(
        event_name, num_codes, out_dir, private_key_file, public_key_file, progress_indicator))
