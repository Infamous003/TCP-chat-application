import socket, threading, sys

FORMAT = "ascii"
DEST_NAME = socket.gethostname()
DEST_IP = socket.gethostbyname(DEST_NAME)
PORT = 50000
BYTE_SIZE = 1024
CONNECTED = True
DISCONNECT_MSG = "quit"

def connect_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((DEST_IP, PORT))
    print("[CONNECTED] Connected to the server.\n")
    return client_socket

def get_user_input():
    connected = True
    while connected:
        msg = input(f"{DEST_NAME}@{DEST_IP}:$ ") or "[EMPTY STRING]"
        if (msg != 'quit()'):
            return msg

def print_server_response(client_socket):
    while True:
        try:
            msg = client_socket.recv(BYTE_SIZE).decode(FORMAT)
            if msg and msg != 'quit()':
                print(f"[SERVER]: {msg}")
            elif msg == 'quit()':
                print("[SERVER SHUTDOWN] Server has shutdown...")
                client_socket.close()
                break
            else:
                break
        except OSError as e:
            print(f"[ERRRRROOORR]: {e}")
            break

def send_message(client_socket):
    while True:
        msg = input() or "[EMPTY STRING]"
        if msg == 'quit()':
            client_socket.send(msg.encode(FORMAT))
            client_socket.close()
            break
        client_socket.send(msg.encode(FORMAT))
        
def main():
    client_socket = connect_client_socket()
    client_thread = threading.Thread(target=send_message, args=(client_socket, ))

    receiver_thread = threading.Thread(target=print_server_response, args=(client_socket, ))
    receiver_thread.start()
    client_thread.start()
    
    receiver_thread.join()
    client_thread.join()

main()