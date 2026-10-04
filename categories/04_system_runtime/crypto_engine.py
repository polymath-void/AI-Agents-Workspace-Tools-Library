#!/usr/bin/env python3
"""
Standard Data Encryption Utility
Demonstrates symmetric encryption for data at rest, similar to standard data protection.
Requires: pip install cryptography
"""

import sys
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def get_key(password: str, salt: bytes) -> bytes:
    """Generate a secure key from a password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_message(password: str, message: str) -> str:
    salt = os.urandom(16)
    key = get_key(password, salt)
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    # Prepend salt to the encrypted message so we can decrypt it later
    return base64.b64encode(salt + encrypted).decode()

def decrypt_message(password: str, token: str) -> str:
    raw_data = base64.b64decode(token.encode())
    salt = raw_data[:16]
    encrypted = raw_data[16:]
    key = get_key(password, salt)
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()

if __name__ == "__main__":
    print("=== Data Protection Encryption Engine ===")
    action = input("Choose action (encrypt/decrypt): ").strip().lower()
    
    if action == "encrypt":
        pwd = input("Enter a secure password: ")
        msg = input("Enter the secret message to encrypt: ")
        encrypted_token = encrypt_message(pwd, msg)
        print("\n[+] Encrypted Data:")
        print(encrypted_token)
        
    elif action == "decrypt":
        pwd = input("Enter the secure password: ")
        token = input("Enter the encrypted token: ")
        try:
            decrypted_msg = decrypt_message(pwd, token)
            print("\n[+] Decrypted Data:")
            print(decrypted_msg)
        except Exception as e:
            print(f"\n[-] Decryption failed. Incorrect password or corrupted data.")
    else:
        print("Invalid action.")
