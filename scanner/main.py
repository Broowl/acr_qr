import crypto
import qr
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("public_key")
    parsed_args = parser.parse_args()
    file_name = parsed_args.file_name
    public_key_file = parsed_args.public_key
    key = crypto.read_key(public_key_file)
    read_message, read_signature = qr.read_signed_message(file_name)
    is_verified = crypto.verify_message(read_message, read_signature, key)
    if is_verified:
        print("Access granted")
    else:
        print("Access denied")