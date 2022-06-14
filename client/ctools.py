import os

import rsa


path = os.path.dirname(os.path.abspath(__file__))

def get_public_key(path: str) -> rsa.PublicKey:
    with open(path, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def encrypt_string(message: str, public_key: rsa.PublicKey) -> bytes:
    return rsa.encrypt(message.encode(), public_key)