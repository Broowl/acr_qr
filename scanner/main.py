import crypto
import qr
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_dir")
    parser.add_argument("public_key")
    parsed_args = parser.parse_args()
    in_dir = parsed_args.in_dir
    public_key_file = parsed_args.public_key

    key = crypto.read_key(public_key_file)
    for file_name in os.listdir(in_dir):
        read_message, read_signature = qr.read_signed_message(os.path.join(in_dir, file_name))
        is_verified = crypto.verify_message(read_message, read_signature, key)
        if is_verified:
            print("Access granted")
        else:
            print("Access denied")