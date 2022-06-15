import os

import rsa

cars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
path = os.path.dirname(os.path.abspath(__file__))


def int_to_base62(i: int) -> str:
    if i == 0: return "0"
    s = ""
    while i > 0:
        s = cars[i % 62] + s
        i //= 62
    return s


def crypt_token(token: str, token_key: rsa.PublicKey) -> str:
    crypted_tocken = "".join([str(e) for e in rsa.encrypt(token.encode(), token_key)])
    print(crypted_tocken)
    s = ""
    nxt = 0
    for i in range(len(crypted_tocken)):
        if nxt == i:
            s += crypted_tocken[i]
            nxt += int(crypted_tocken[i]) + 1

    return int_to_base62(int(s))


def get_private_key(path: str) -> rsa.PrivateKey:
    with open(path, "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

def get_public_key(path: str) -> rsa.PublicKey:
    with open(path, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())


def check_user(token: str, users: list, token_key: rsa.PublicKey):
    ctoken = crypt_token(token, token_key)
    print(ctoken)
    return next((user for user in users if user["ctoken"] == ctoken), None)


def decrypt_data(data: bytes, psw_key: rsa.PrivateKey) -> str:
    sortie = []
    for e in data.decode().split("<end>")[:-1]:
        if e[:2] in ["b'", "b\""] and e[-1:] in ["'", "\""]:
            sortie.append(decrypt_message(eval(e), psw_key))
        else: print(f"ERREUR: {e}")
    return sortie


def decrypt_message(message: bytes, private_key: rsa.PrivateKey) -> str:
    return rsa.decrypt(message, private_key).decode()
