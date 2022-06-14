import os

import rsa


path = os.path.dirname(os.path.abspath(__file__))

def get_private_key(path: str) -> rsa.PrivateKey:
    with open(path, "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

def decrypt_message(message: bytes, private_key: rsa.PrivateKey) -> str:
    return rsa.decrypt(message, private_key).decode()