import socket
import time
import threading
import sys

FORMAT = "utf-8"
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
PORT = 50000
BYTE_SIZE = 1024
LOADING_STRING = "..."
CLIENT_SOCKET_LIST = []
CLIENT_THREAD_LIST = []

def create_server_socket():
    server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_Socket.bind((HOST_IP, PORT))
    server_Socket.listen()
    return server_Socket

def create_client_socket(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"[CONNECTED] Client: {client_address[0]} connected...\n")
    return [client_socket, client_address]

def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(BYTE_SIZE).decode(FORMAT)
            if msg:
                print(f"[CLIENT]: {msg}")
        except ConnectionResetError:
            break



def loading():
    print(f"[LISTENING] Server listening", end='', flush=True)
    for i in range(3):
        print(".", end='', flush=True)
        time.sleep(1)
    print()

def send_message(client_socket):
    while True:
        msg = input(f"{HOST_IP}:$") or "[EMPTY STRING]"
        if msg == 'quit()':
            client_socket.send(msg.encode(FORMAT))
            client_socket.close()
            break
        client_socket.send(msg.encode(FORMAT))



def main():
    CONNECTED = True
    server_socket = create_server_socket()
    loading()  

    client_socket, client_address = create_client_socket(server_socket)
    send_thread = threading.Thread(target=send_message, args=(client_socket, ))

    client_thread = threading.Thread(target=handle_client, args=(client_socket, ))
    client_thread.start()
    print("ACTIVE: ", threading.active_count()-1)
    send_thread.start()

    client_thread.join()
    send_thread.join()
    
main()