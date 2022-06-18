import json

import ctools as ct
from POOcom import ClientCom

token = json.load(open(f"{ct.path}/token.json"))[input("username: ")]
psw_key = ct.get_public_key(f"{ct.path}/keys/psw_public.pem")
clt_key = ct.get_public_key(f"{ct.path}/keys/clt_public.pem")
srv_key = ct.get_private_key(f"{ct.path}/keys/srv_private.pem")

client = ClientCom(host="localhost", port=57321)

client.send(ct.encrypt_string(token, psw_key))

@client.on_message
def on_message(data):
    print(ct.decrypt_data(data, srv_key))

while True:
    msg = input()
    client.send(ct.encrypt_string(msg, clt_key))
