import rsa
import os

# Generate a public/private key pair and

path = os.path.dirname(os.path.abspath(__file__))

def generate_keys(name):
    print(f"Generating keys for {name}")
    public_key, private_key = rsa.newkeys(2048)

    # Save the private key to a file
    with open(f"{path}/keys/{name}_private.pem", "wb") as f:
        f.write(private_key.save_pkcs1())

    # Save the public key to a file
    with open(f"{path}/keys/{name}_public.pem", "wb") as f:
        f.write(public_key.save_pkcs1())

try: os.mkdir(f"{path}/keys")
except FileExistsError: pass

generate_keys("psw")
generate_keys("token")