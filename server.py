import socket
import time
import threading

FORMAT = "utf-8"
HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
PORT = 50005
CONNECTED = True
BYTE_SIZE = 1024
LOADING_STRING = "..."
# result = [None]

def create_server_socket():
    # global result
    server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_Socket.bind((HOST_IP, PORT))
    server_Socket.listen()
    # result.append(server_Socket)
    # print("result::::", result)
    return server_Socket

def create_client_socket(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"[CONNECTED] Client: {client_address[0]} connected...\n")
    return [client_socket, client_address]
    # return client_socket

def get_client_message(client_socket):
    client_message = client_socket.recv(BYTE_SIZE).decode()
    return client_message

def handle_client_msg(client_socket):
    global CONNECTED
    while CONNECTED:
        client_msg = get_client_message(client_socket)
        print(f"[CLIENT]:$ {client_msg}")
        if client_msg != "quit":
            msg = input(f"{HOST_NAME}@{HOST_IP}:$ ") or "[EMPTY STRING]"
            client_socket.send(msg.encode(FORMAT))
            print(f"[SENT] Message sent...")
            continue
        else:
            CONNECTED = False


def loading():
    print(f"[LISTENING] Server listening", end='', flush=True)
    for i in range(3):
        print(".", end='', flush=True)
        time.sleep(1)
    print()

def main():
    server_socket = create_server_socket()
    loading()
    client_socket, client_address = create_client_socket(server_socket)
    handle_client_msg(client_socket)

    print(f"[SHUTDOWN] Server has shut down...")
    server_socket.close()
    
main()