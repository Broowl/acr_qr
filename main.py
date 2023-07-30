import crypto
import qr

if __name__ == "__main__":
    message = "Architects"
    file_name = "qr.png"
    key = crypto.generate()
    signature = crypto.sign_message(message, key)
    qr.save_signed_message(message, signature, file_name)
    read_message, read_signature = qr.read_signed_message(file_name)
    is_verified = crypto.verify_message(
        read_message, read_signature, key.public_key())
    if is_verified:
        print("Access granted")
    else:
        print("Access denied")
