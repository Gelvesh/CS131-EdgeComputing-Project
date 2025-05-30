from cryptography.fernet import Fernet
import os

KEY_PATH = 'cloud/secret.key'

def load_key():
    with open(KEY_PATH, 'rb') as key_file:
        return key_file.read()

fernet = Fernet(load_key())

def decrypt_file(path):
    with open(path, 'rb') as f:
        encrypted_data = f.read()
    return fernet.decrypt(encrypted_data)

def decrypt_text(path):
    return decrypt_file(path).decode()

def decrypt_and_save_all():
    os.makedirs("decrypted", exist_ok=True)

    # Decrypt image
    decrypted_image = decrypt_file("downloaded/encrypted_image.bin")
    with open("decrypted/alert.jpg", "wb") as f:
        f.write(decrypted_image)
    print("Decrypted image saved to decrypted/alert.jpg")

    # Decrypt log
    decrypted_log = decrypt_text("downloaded/encrypted_log.txt")
    with open("decrypted/alert_log.txt", "w") as f:
        f.write(decrypted_log)
    print("Decrypted log saved to decrypted/alert_log.txt")

if __name__ == "__main__":
    decrypt_and_save_all()
