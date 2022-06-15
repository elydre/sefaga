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
fenettre.geometry("600x400")

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

# tkinter functions

tk_srv_msg = tk.Label(fenettre)
tk_usr_msg = tk.Label(fenettre)
tk_usr_oln = tk.Label(fenettre)
tk_srv_ifo = tk.Label(fenettre)
tk_srv_inp = tk.Entry(fenettre, bd=0)
tk_drk_mod = tk.Button(fenettre, text="artemis", bd = 0, command = lambda: change_theme())

def set_theme(text: str, window: str, label: str) -> None:
    for e in [tk_srv_msg, tk_usr_msg, tk_usr_oln, tk_srv_ifo, tk_srv_inp, tk_drk_mod]:
        e.config(bg=label, fg=text, font=("Arial", 13))
    fenettre.config(bg=window)

def change_theme() -> None:
    if tk_drk_mod.cget("text") == "artemis":
        set_theme("#ffffff", "#1e1e1e", "#333333")
        tk_srv_inp.config(insertbackground="#ffffff")
        tk_drk_mod.config(text="salaud")
    else:
        set_theme("#000000", "#f0f0f0", "#ffffff")
        tk_srv_inp.config(insertbackground="#000000")
        tk_drk_mod.config(text="artemis")

def update_tk(old: tuple) -> None:
    fx = fenettre.winfo_width()
    fy = fenettre.winfo_height()


    if (fx, fy) != old:
        print(fx, fy)
        tk_srv_msg.place(x=5, y=5, width=fx//3-10, height=fy-50)
        tk_usr_msg.place(x=fx//3, y=5, width=fx//3-5, height=fy-50)
        tk_usr_oln.place(x=fx//3*2, y=5, width=fx//3-5, height=fy//2-10)
        tk_srv_ifo.place(x=fx//3*2, y=fy//2, width=fx//3-5, height=fy//2-75)
        tk_srv_inp.place(x=5, y=fy-40, width=fx-10, height=30)
        tk_drk_mod.place(x=fx//3*2, y=fy-70, width=fx//3-5, height=25)
    
    fenettre.after(100, lambda: update_tk((fx, fy)))

change_theme()
update_tk((1, 1))

# start_new_thread(start_server, ())

fenettre.mainloop()
