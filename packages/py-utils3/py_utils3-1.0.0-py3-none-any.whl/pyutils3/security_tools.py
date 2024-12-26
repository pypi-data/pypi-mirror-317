# smart_library/security_tools.py
import random
import string
from cryptography.fernet import Fernet

def generate_password(length=12):
    """Generate a random strong password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt_data(data):
    """Encrypt data using Fernet encryption."""
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data, key

def decrypt_data(encrypted_data, key):
    """Decrypt encrypted data using Fernet."""
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data
