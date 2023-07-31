import crypto
import qr
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event_name")
    parser.add_argument("out_dir")
    parser.add_argument("num_codes")
    parser.add_argument("-puk", "--public_key")
    parser.add_argument("-prk", "--private_key")
    parsed_args = parser.parse_args()
    event_name = parsed_args.event_name
    out_dir = parsed_args.out_dir
    num_codes = int(parsed_args.num_codes)
    public_key_file = parsed_args.public_key
    private_key_file = parsed_args.private_key

    key = crypto.generate_or_get_keys(private_key_file, public_key_file)
    for i_code in range(num_codes):
        data = f"{event_name}_{i_code}"
        signature = crypto.sign_message(data, key)
        qr.save_signed_message(data, signature, os.path.join(
            out_dir, event_name, f"{i_code}.png"))
