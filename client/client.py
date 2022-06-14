import ctools as ct
from POOcom import ClientCom

client = ClientCom(host="localhost", port=57321)

psw_key = ct.get_public_key(f"{ct.path}/keys/psw_public.pem")

client.send(ct.encrypt_string("coucou", psw_key))
