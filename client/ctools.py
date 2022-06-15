import os

import rsa


path = os.path.dirname(os.path.abspath(__file__))

# shared functions

def get_private_key(path: str) -> rsa.PrivateKey:
    with open(path, "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())


def get_public_key(path: str) -> rsa.PublicKey:
    with open(path, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())


def decrypt_message(message: bytes, private_key: rsa.PrivateKey) -> str:
    return rsa.decrypt(message, private_key).decode()


def encrypt_string(message: str, public_key: rsa.PublicKey) -> bytes:
    return rsa.encrypt(message.encode(), public_key)

# ctools functions

def decrypt_data(data: str, psw_key: rsa.PrivateKey) -> str:
    if data[:2] in ["b'", "b\""] and data[-1:] in ["'", "\""]:
        return decrypt_message(eval(data), psw_key)
    else: print(f"ERREUR: {data}")