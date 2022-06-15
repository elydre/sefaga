import os
import random

import rsa

cars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


path = os.path.dirname(os.path.abspath(__file__))
token_key = rsa.PublicKey.load_pkcs1(open(f"{path}/keys/token_public.pem").read())

new_token = lambda: "".join([random.choice(cars) for _ in range(20)])


def int_to_base62(i: int) -> str:
    if i == 0: return "0"
    s = ""
    while i > 0:
        s = cars[i % 62] + s
        i //= 62
    return s


def crypt_token(token: str) -> str:
    crypted_tocken = "".join([str(e) for e in rsa.encrypt(token.encode(), token_key)])
    s = ""
    nxt = 0
    for i in range(len(crypted_tocken)):
        if nxt == i:
            s += crypted_tocken[i]
            nxt += int(crypted_tocken[i]) + 1

    return int_to_base62(int(s))


def generate_token():
    token = new_token()
    print(f"Clear token: {token}")
    crypted_tocken = crypt_token(token)

    print(f"Crypted token: {crypted_tocken}")


generate_token()
