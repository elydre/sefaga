import json
import tkinter as tk

import ctools as ct
from POOcom import ClientCom

username = input("username: ")
tokens = json.load(open(f"{ct.path}/token.json"))
psw_key = ct.get_public_key(f"{ct.path}/keys/psw_public.pem")
clt_key = ct.get_public_key(f"{ct.path}/keys/clt_public.pem")
srv_key = ct.get_private_key(f"{ct.path}/keys/srv_private.pem")
username = "user" if username not in tokens.keys() else username
token = tokens[username]

# tkinter
fenettre = tk.Tk()
fenettre.title("sefaga client")
fenettre.geometry("600x400")

tk_msg = tk.Text(fenettre, bd=0)
tk_inp = tk.Entry(fenettre, bd=0)
tk_mod = tk.Button(fenettre, text="artemis", bd = 0, command = lambda: change_theme())
tk_msg.config(state="disabled")

# client com
client = ClientCom(host="localhost", port=57321)
client.send(ct.encrypt_string(token, psw_key))

def add_msg(msg) -> None:
    tk_msg.config(state="normal")
    tk_msg.insert("0.0", f"{msg}\n")
    tk_msg.config(state="disabled")

@client.on_message
def on_message(data):
    add_msg(ct.decrypt_data(data, srv_key))

def on_input(event):
    msg = tk_inp.get()
    if msg == "": return
    add_msg(f"{username}: {msg}")
    tk_inp.delete(0, "end")
    client.send(ct.encrypt_string(msg, clt_key))

tk_inp.bind("<Return>", on_input)


def set_theme(text: str, window: str, label: str) -> None:
    for e in [tk_msg, tk_mod, tk_inp]:
        e.config(bg=label, fg=text, font=("Arial", 13))
    fenettre.config(bg=window)

def change_theme() -> None:
    if tk_mod.cget("text") == "artemis":
        set_theme("#ffffff", "#1e1e1e", "#333333")
        tk_inp.config(insertbackground="#ffffff")
        tk_mod.config(text="salaud")
    else:
        set_theme("#000000", "#f0f0f0", "#ffffff")
        tk_inp.config(insertbackground="#000000")
        tk_mod.config(text="artemis")


def update_tk(old: tuple) -> None:
    fx = fenettre.winfo_width()
    fy = fenettre.winfo_height()

    if (fx, fy) != old:
        print(fx, fy)
        tk_msg.place(x=5, y=5, width=fx-10, height=fy-50)
        tk_inp.place(x=5, y=fy-40, width=fx//5*4-10, height=30)
        tk_mod.place(x=fx//5*4, y=fy-40, width=fx//5-5, height=30)
    
    fenettre.after(100, lambda: update_tk((fx, fy)))

change_theme()
update_tk((1, 1))

fenettre.mainloop()
