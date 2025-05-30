# cloud/encrypt_utils.py

from cryptography.fernet import Fernet
import os

# Paths
KEY_PATH = 'cloud/secret.key'
IMAGE_INPUT = 'alert_image/alert.jpg'
LOG_INPUT = 'logs/alert_log.txt'
ENC_IMAGE_OUTPUT = 'encrypted/encrypted_image.bin'
ENC_LOG_OUTPUT = 'encrypted/encrypted_log.txt'

# Generate/load encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_PATH):
        return generate_key()
    with open(KEY_PATH, 'rb') as f:
        return f.read()

fernet = Fernet(load_key())

# Encryption functions
def encrypt_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(output_path, 'wb') as f:
        f.write(encrypted)

def encrypt_text(input_path, output_path):
    with open(input_path, 'r') as f:
        text = f.read()
    encrypted = fernet.encrypt(text.encode())
    with open(output_path, 'wb') as f:
        f.write(encrypted)

# === Main execution ===
if __name__ == "__main__":
    os.makedirs('encrypted', exist_ok=True)
    encrypt_file(IMAGE_INPUT, ENC_IMAGE_OUTPUT)
    print(f"Encrypted image → {ENC_IMAGE_OUTPUT}")
    encrypt_text(LOG_INPUT, ENC_LOG_OUTPUT)
    print(f"Encrypted log → {ENC_LOG_OUTPUT}")
