import hashlib
import os
import random

cars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

path = os.path.dirname(os.path.abspath(__file__))

new_token = lambda: "".join([random.choice(cars) for _ in range(20)])  


def crypt_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_token():
    token = new_token()
    print(f"Clear: {token}")
    crypted_tocken = crypt_token(token)

    print(f"Crypt: {crypted_tocken}")


generate_token()
