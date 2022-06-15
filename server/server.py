import json
import socket
from _thread import start_new_thread
import tkinter as tk

import stools as st


# server ip and port
HOST = "localhost"
PORT = 57321

# rsa keys
psw_key = st.get_private_key(f"{st.path}/keys/psw_private.pem")
clt_key = st.get_private_key(f"{st.path}/keys/clt_private.pem")
srv_key = st.get_public_key(f"{st.path}/keys/srv_public.pem")

# json user list
users = json.load(open(f"{st.path}/users.json"))

# server data
SD = {
    "online_users": {},
    "user_messages": [],
    "srv_messages": []
}

# tkinter
fenettre = tk.Tk()
fenettre.title("sefaga server")



# socket server functions

def stop_user(conn: socket.socket) -> None:
    SD["srv_messages"].append(f"{SD['online_users'][conn]['addr']} disconnected from socket")
    del SD["online_users"][conn]
    conn.close()


def login_user(conn: socket.socket, addr: tuple) -> None:
    str_addr = f"{addr[0]}:{addr[1]}"

    SD["srv_messages"].append(f"{str_addr} connected to socket")

    SD["online_users"][conn] = {
        "addr": str_addr,
        "loged": False,
        "name": None,
        "plvl": None,
        "conn": conn
    }

    try:
        data = conn.recv(1024)
        if not data: return conn.close()
    except ConnectionResetError:
        return stop_user(conn)
    
    dd = st.decrypt_data(data, psw_key)[0]
    SD["srv_messages"].append(f"{str_addr} token: {dd}")        # dev only, not safe
    
    if user := st.check_user(dd, users):
        if user["name"] in [u["name"] for u in SD["online_users"].values()]:
            SD["srv_messages"].append(f"{user['name']} is already loged")
            conn.send(f"{st.encrypt_string('server: user already loged', srv_key)}<end>".encode())
            return stop_user(conn)
        
        SD["srv_messages"].append(f"{str_addr} user name: {user['name']}")
        
        SD["online_users"][conn]["name"] = user["name"]
        SD["online_users"][conn]["plvl"] = user["plvl"]
        SD["online_users"][conn]["loged"] = True

        user_com(conn)
        SD["srv_messages"].append(f"{user['name']} quited")
    else:
        SD["srv_messages"].append(f"{str_addr} invalid token")
        
    return stop_user(conn)


def user_com(conn: socket.socket) -> None:
    user_name = SD["online_users"][conn]["name"]
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            dd = st.decrypt_data(data, clt_key)[0]
            msg = f"{user_name}: {dd}"
            SD["user_messages"].append(msg)
            for u in SD["online_users"].values():
                if u["loged"] and u["name"] != user_name:
                    u["conn"].send(f"{st.encrypt_string(msg, srv_key)}<end>".encode())
        except ConnectionResetError:
            break

def start_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        SD["srv_messages"].append("Socket créé")
        s.listen()
        while True:
            SD["srv_messages"].append("Attente de connexion...")
            conn, addr = s.accept()
            start_new_thread(login_user, (conn, addr))

