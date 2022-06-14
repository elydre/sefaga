import socket
from _thread import start_new_thread
import stools as st
import rsa

HOST = "localhost"      # server ip
PORT = 57321            # server port

psw_key = st.get_private_key(f"{st.path}/keys/psw_private.pem")
token_key = st.get_public_key(f"{st.path}/keys/token_public.pem")

def decrypt_data(data: bytes) -> str:
    sortie = []
    for e in data.decode().split("<end>")[:-1]:
        if e[:2] in ["b'", "b\""] and e[-1:] in ["'", "\""]:
            sortie.append(st.decrypt_message(eval(e), psw_key))
        else: print(f"ERREUR: {e}")
    return sortie

def check_user(tocken: str, users: list):
    crypted_tocken = "".join([str(e) for e in rsa.encrypt(tocken, token_key)])
    return next((user for user in users if user["token"] == tocken), False)

def login_user(conn: socket.socket, addr: tuple):
    print(f"**{addr[0]}~{addr[1]} c'est connecte!**")
    try:
        data = conn.recv(1024)
        if not data: return
    except Exception as e:
        print(e)
        conn.close()
        return
    print(decrypt_data(data))
    print(f"**{addr[0]}~{addr[1]} c'est déconnecte**")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("**Socket créé**")
    s.listen()
    while True:
        print("Attente de connexion...")
        conn, addr = s.accept()
        start_new_thread(login_user, (conn, addr))
