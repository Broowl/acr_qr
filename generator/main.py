import crypto
import qr
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event_name")
    parser.add_argument("file_name")
    parser.add_argument("-puk", "--public_key")
    parser.add_argument("-prk", "--private_key")
    parsed_args = parser.parse_args()
    event_name = parsed_args.event_name
    file_name = parsed_args.file_name
    public_key_file = parsed_args.public_key
    private_key_file = parsed_args.private_key
    args = parser.parse_args()
    key = crypto.generate_or_get_keys(private_key_file, public_key_file)
    signature = crypto.sign_message(event_name, key)
    qr.save_signed_message(event_name, signature, file_name)
