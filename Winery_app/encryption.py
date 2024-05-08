from cryptography.fernet import Fernet
import os

key_file_path = "encryption_key.bin"
key = None

def save_key_to_file( file_path):
    global key
    with open(file_path, "wb") as file:
            file.write(key)


def load_key_from_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message):
    global key
    if not os.path.exists(key_file_path):
        key = generate_key()
        save_key_to_file(key_file_path)
    else:
        key = load_key_from_file(key_file_path)
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(message)

def decrypt_message(encrypted_message):
    if not os.path.exists(key_file_path):
        return "No key file found"
    key = load_key_from_file(key_file_path)
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_message)