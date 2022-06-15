import hashlib
import os

import rsa

path = os.path.dirname(os.path.abspath(__file__))


def crypt_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def get_private_key(path: str) -> rsa.PrivateKey:
    with open(path, "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())


def get_public_key(path: str) -> rsa.PublicKey:
    with open(path, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())


def check_user(token: str, users: list):
    return next((user for user in users if user["ctoken"] == crypt_token(token)), None)


def decrypt_data(data: bytes, psw_key: rsa.PrivateKey) -> str:
    sortie = []
    for e in data.decode().split("<end>")[:-1]:
        if e[:2] in ["b'", "b\""] and e[-1:] in ["'", "\""]:
            sortie.append(decrypt_message(eval(e), psw_key))
        else: print(f"ERREUR: {e}")
    return sortie


def decrypt_message(message: bytes, private_key: rsa.PrivateKey) -> str:
    return rsa.decrypt(message, private_key).decode()
