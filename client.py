import socket

FORMAT = "ascii"
DEST_NAME = socket.gethostname()
DEST_IP = socket.gethostbyname(DEST_NAME)
PORT = 50005
BYTE_SIZE = 1024
CONNECTED = True
DISCONNECT_MSG = "quit"

def connect_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((DEST_IP, PORT))
    print("[CONNECTED] Client connected\n")
    return client_socket

def get_user_input():
    msg = input(f"{DEST_NAME}@{DEST_IP}:$ ") or "[EMPTY STRING]"
    return msg

def main():
    global CONNECTED
    client_socket = connect_client_socket()
    while CONNECTED:
        msg = get_user_input()
        client_socket.send(msg.encode(FORMAT))
        if msg != "quit":
            print("[SENT] Message sent...\n")
            server_reply = client_socket.recv(BYTE_SIZE).decode(FORMAT)
            print(f"[SERVER]:$ {server_reply}")
            continue
        else:
            CONNECTED = False
            break
    print(f"[SHUTDOWN] Client has shutdown...")
    client_socket.close()
main()