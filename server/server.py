import socket
from _thread import start_new_thread
import stools as st

HOST = "localhost"      # server ip
PORT = 57321            # server port

psw_key = st.get_private_key(f"{st.path}/keys/psw_private.pem")

liste_conn = []

def decrypt_data(data: bytes) -> str:
    sortie = []
    for e in data.decode().split("<end>")[:-1]:
        if e[:2] in ["b'", "b\""] and e[-1:] in ["'", "\""]:
            sortie.append(st.decrypt_message(eval(e), psw_key))
        else:
            print(f"ERREUR: {e}")
    return sortie

def echange(conn: socket.socket, addr: tuple):
    print(type(conn), type(addr))
    with conn:
        print(f"**{addr[0]}~{addr[1]} c'est connecte!**")
        liste_conn.append([conn, addr])
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
            except Exception as e:
                print(e)
                conn.close()
                break
            print(decrypt_data(data))
    liste_conn.remove([conn, addr])
    print(f"**{addr[0]}~{addr[1]} c'est déconnecte**")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("**Socket créé**")
    s.listen()
    while True:
        print("Attente de connexion...")
        conn, addr = s.accept()
        start_new_thread(echange, (conn, addr))
