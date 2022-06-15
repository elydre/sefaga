import json
import socket
from _thread import start_new_thread

import stools as st


HOST = "localhost"      # server ip
PORT = 57321            # server port

psw_key = st.get_private_key(f"{st.path}/keys/psw_private.pem")
clt_key = st.get_private_key(f"{st.path}/keys/clt_private.pem")
srv_key = st.get_public_key(f"{st.path}/keys/srv_public.pem")


users = json.load(open(f"{st.path}/users.json"))

online_users = []

def login_user(conn: socket.socket, addr: tuple) -> None:
    print(f"{addr[0]}:{addr[1]} send login request")

    data = conn.recv(1024)
    if not data: return conn.close()
    
    dd = st.decrypt_data(data, psw_key)[0]
    print(f"{addr[0]}:{addr[1]} token: {dd}")         # dev only, not safe
    
    if user := st.check_user(dd, users):
        print(f"{addr[0]}:{addr[1]} user name: {user['name']}")
        user["ip"], user["port"], user["conn"] = addr[0], addr[1], conn
        user_com(user)
        print(f"{addr[0]}:{addr[1]} logout")
    else:
        print(f"{addr[0]}:{addr[1]} invalid token")
        return conn.close()


def user_com(user: dict) -> None:
    online_users.append(user)
    conn = user["conn"]
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            dd = st.decrypt_data(data, clt_key)[0]
            msg = f"{user['name']}: {dd}"
            print(msg)
            for u in online_users:
                if u["name"] != user["name"]:
                    u["conn"].send(f"{st.encrypt_string(msg, srv_key)}<end>".encode())
        except ConnectionResetError:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Socket créé")
    s.listen()
    while True:
        print("Attente de connexion...")
        conn, addr = s.accept()
        start_new_thread(login_user, (conn, addr))
