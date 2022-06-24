import json
import socket
import tkinter as tk
from _thread import start_new_thread

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
fenettre.geometry("1000x600")

# socket server functions

def stop_user(conn: socket.socket, reason: str) -> None:

    SD["srv_messages"].append(f"{SD['online_users'][conn]['addr']}: {reason}\n{SD['online_users'][conn]['addr']} disconnected from socket")
    del SD["online_users"][conn]
    conn.close()

def login_user(conn: socket.socket, addr: tuple) -> None:
    str_addr = f"{addr[0]}:{addr[1]}"

    SD["srv_messages"].append(f"{str_addr} connected to socket")

    SD["online_users"][conn] = {
        "addr": str_addr,
        "loged": False,
        "name": None,
        "conn": conn
    }

    try:
        data = conn.recv(1024)
        if not data: return stop_user(conn, "no data")
    except ConnectionResetError:
        return stop_user(conn, "connection reset")
    
    dd = st.decrypt_data(data, psw_key)[0]
    if not dd: return stop_user(conn, "decryption error")
    SD["srv_messages"].append(f"{str_addr} token: {dd}")        # dev only, not safe
    
    if user := st.check_user(dd, users):
        if user["name"] in [u["name"] for u in SD["online_users"].values()]:
            conn.send(f"{st.encrypt_string('server: user already loged', srv_key)}<end>".encode())
            return stop_user(conn, f"{user['name']} user already loged")
        
        SD["srv_messages"].append(f"{str_addr} user name: {user['name']}")
        
        SD["online_users"][conn]["name"] = user["name"]
        SD["online_users"][conn]["loged"] = True

        user_com(conn)
        SD["srv_messages"].append(f"{user['name']} quited")
        send_all(f"{user['name']} quited")
    else:
        SD["srv_messages"].append(f"{str_addr} invalid token")
        
    return stop_user(conn, "connection closed")

def user_com(conn: socket.socket) -> None:
    user_name = SD["online_users"][conn]["name"]
    send_all(f"server: {user_name} is online")
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            dd = st.decrypt_data(data, clt_key)[0]
            if not dd: break
            msg = f"{user_name}: {dd}"
            SD["user_messages"].append(msg)
            for u in SD["online_users"].values():
                if u["loged"] and u["name"] != user_name:
                    u["conn"].send(f"{st.encrypt_string(msg, srv_key)}<end>".encode())
        except ConnectionResetError:
            break

def send_all(msg) -> None:
    SD["user_messages"].append(msg)
    for u in SD["online_users"].values():
        if u["loged"] and u["name"]:
            u["conn"].send(f"{st.encrypt_string(msg, srv_key)}<end>".encode())


def start_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        SD["srv_messages"].append("Socket créé")
        s.listen()
        while True:
            SD["srv_messages"].append("Attente de connexion...")
            conn, addr = s.accept()
            start_new_thread(login_user, (conn, addr))

# tkinter setup & functions

def on_input(event):
    msg = f"server: {tk_srv_inp.get()}"
    send_all(msg)

    tk_srv_inp.delete(0, "end")

tk_srv_msg = tk.Text(fenettre, bd=0)
tk_usr_msg = tk.Text(fenettre, bd=0)
tk_usr_oln = tk.Label(fenettre, anchor="n")
tk_srv_ifo = tk.Label(fenettre, anchor="n")
tk_srv_inp = tk.Entry(fenettre, bd=0)
tk_drk_mod = tk.Button(fenettre, text="artemis", bd = 0, command = lambda: change_theme())
tk_srv_inp.bind("<Return>", on_input)

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
        tk_srv_msg.place(x=5, y=5, width=fx//5*2-10, height=fy-50)
        tk_usr_msg.place(x=fx//5*2, y=5, width=fx//5*2-5, height=fy-50)
        tk_usr_oln.place(x=fx//5*4, y=5, width=fx//5-5, height=fy//2-10)
        tk_srv_ifo.place(x=fx//5*4, y=fy//2, width=fx//5-5, height=fy//2-75)
        tk_drk_mod.place(x=fx//5*4, y=fy-70, width=fx//5-5, height=25)
        tk_srv_inp.place(x=5, y=fy-40, width=fx-10, height=30)
    
    fenettre.after(100, lambda: update_tk((fx, fy)))


def refresh_labels() -> None:

    sm = "\n".join(SD["srv_messages"][::-1])
    um = "\n".join(SD["user_messages"][::-1])
    ou = "\n\n".join(f"{u['addr']}\n{u['name']}" for u in SD["online_users"].values() if u["loged"])
    fo = "\n\n".join(f"{u['addr']}" for u in SD["online_users"].values() if not u["loged"])

    tk_srv_msg.config(state="normal")
    tk_srv_msg.delete("1.0", "end")
    tk_srv_msg.insert("end", sm)
    tk_srv_msg.config(state="disabled")

    tk_usr_msg.config(state="normal")
    tk_usr_msg.delete("1.0", "end")
    tk_usr_msg.insert("end", um)
    tk_usr_msg.config(state="disabled")

    tk_usr_oln.config(text=ou)
    tk_srv_ifo.config(text=fo)

    fenettre.after(100, lambda: refresh_labels())

change_theme()
update_tk((1, 1))
refresh_labels()

start_new_thread(start_server, ())

fenettre.mainloop()
