import json
import socket
from _thread import start_new_thread

import stools as st


HOST = "localhost"      # server ip
PORT = 57321            # server port

psw_key = st.get_private_key(f"{st.path}/keys/psw_private.pem")
users = json.load(open(f"{st.path}/users.json"))

print(st.crypt_token("V1V7ovvUaCQSLVp92LM9"))

def login_user(conn: socket.socket, addr: tuple):
    print(f"{addr[0]} c'est connecte!")
    try:
        data = conn.recv(1024)
        if not data: return
    except Exception as e:
        print(e)
        conn.close()
        return
    
    dd = st.decrypt_data(data, psw_key)[0]
    print(f"{addr[0]} token: {dd}")
    
    if user := st.check_user(dd, users):
        print(f"{addr[0]} user: {user}")
    else:
        print(f"{addr[0]} token invalide")

    conn.close()
    print(f"{addr[0]} c'est déconnecte")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Socket créé")
    s.listen()
    while True:
        print("Attente de connexion...")
        conn, addr = s.accept()
        start_new_thread(login_user, (conn, addr))
