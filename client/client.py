import json

import ctools as ct
from POOcom import ClientCom

token = json.load(open("token.json"))["token"]
psw_key = ct.get_public_key(f"{ct.path}/keys/psw_public.pem")

client = ClientCom(host="localhost", port=57321)

client.send(ct.encrypt_string(token, psw_key))
