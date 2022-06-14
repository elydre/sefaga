import rsa, os, random

path = os.path.dirname(os.path.abspath(__file__))

cars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

token_key = rsa.PublicKey.load_pkcs1(open(f"{path}/keys/token_public.pem").read())

new_token = lambda: "".join([random.choice(cars) for _ in range(20)])

def generate_token():
    token = new_token()
    print(f"Clear token: {token}")
    crypted_tocken = "".join([str(e) for e in rsa.encrypt(token.encode(), token_key)])
    s = ""
    nxt = 0
    for i in range(len(crypted_tocken)):
        if nxt == i:
            s += crypted_tocken[i]
            nxt += int(crypted_tocken[i]) + 1


    print(f"Crypted token: {s}")

generate_token()