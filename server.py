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
IS_CLIENT_CONNECTED = False

def create_server_socket():
    server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_Socket.bind((HOST_IP, PORT))
    server_Socket.listen()
    return server_Socket

def create_client_socket(server_socket):
    client_socket, client_address = server_socket.accept()
    global IS_CLIENT_CONNECTED
    IS_CLIENT_CONNECTED  = True
    print("AFter creatiion",IS_CLIENT_CONNECTED)
    print(f"[CONNECTED] Client: {client_address[0]} connected...\n")
    return [client_socket, client_address]

def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(BYTE_SIZE).decode(FORMAT)
            if msg:
                if msg == 'quit()':
                    global IS_CLIENT_CONNECTED
                    print(f"[CLIENT]: {msg} \n[CLIENT DISCONNECTED]")
                    client_socket.close()
                    IS_CLIENT_CONNECTED = False
                    break
                else:
                    print(f"[CLIENT]: {msg}")
        except ConnectionResetError:
            print(f"[ERROR]: Connection reset by client")
            break

def loading():
    print(f"[LISTENING] Server listening", end='', flush=True)
    for i in range(3):
        print(".", end='', flush=True)
        time.sleep(1)
    print()

def send_message(client_socket):
    global IS_CLIENT_CONNECTED
    while IS_CLIENT_CONNECTED:  # Only allow sending messages if a client is connected
        try:
            if IS_CLIENT_CONNECTED:
                msg = input() or "[EMPTY STRING]"
            else:
                print("BREAKING")
                break
            if msg == 'quit()':
                client_socket.send(msg.encode(FORMAT))
                client_socket.close()
                server_socket.close()  # Close the server socket if the server quits
                print('[SERVER SHUTDOWN] Shutting down...')
                break
            elif IS_CLIENT_CONNECTED and client_socket:  # Send message only if client is connected
                client_socket.send(msg.encode(FORMAT))
            else:
                break
        except OSError as e:
            print(f"[ERROR]: {e}")
            break
    print("[INFO] Client disconnected, stopping input.")

"""    
def send_message(client_socket):
    global IS_CLIENT_CONNECTED, thread_should_run
    while IS_CLIENT_CONNECTED and thread_should_run:
        try:
            msg = input() or "[EMPTY STRING]"
            if msg == 'quit()':
                client_socket.send(msg.encode(FORMAT))
                client_socket.close()
                server_socket.close()
                print('[SERVER SHUTDOWN] Shutting down...')
                IS_CLIENT_CONNECTED = False
                thread_should_run = False  # Stop the thread after shutdown
                break
            elif IS_CLIENT_CONNECTED:  # Only send if client is connected
                client_socket.send(msg.encode(FORMAT))
        except OSError as e:
            print(f"[ERROR]: {e}")
            break
    print("[INFO] Send thread exiting...")
"""


server_socket = create_server_socket()

loading()

def main():
    global IS_CLIENT_CONNECTED
    while True:
        client_socket, client_address = create_client_socket(server_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

        # Only start the send_thread if the client is connected
        
        if client_thread.is_alive():
            send_thread = threading.Thread(target=send_message, args=(client_socket,))
    
            while client_thread.is_alive():
                if not send_thread.is_alive() and IS_CLIENT_CONNECTED:
                    send_thread.start()

        # Wait for client to disconnect
        client_thread.join()
        IS_CLIENT_CONNECTED = False  # Mark client as disconnected
        print('Client disconnected. Waiting for a new client...')

"""
def main():
    global IS_CLIENT_CONNECTED, thread_should_run
    send_thread = None  # Keep track of the send thread

    while True:
        client_socket, client_address = create_client_socket(server_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, ))

        # Start client thread to handle incoming messages
        client_thread.start()

        # If a send thread exists from the previous client, wait for it to finish
        if send_thread and send_thread.is_alive():
            thread_should_run = False  # Signal the old thread to stop
            send_thread.join()

        # Reset the flag and start a new send thread for the new client
        thread_should_run = True
        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        send_thread.start()

        # Wait for client thread to finish
        client_thread.join()

        # When the client disconnects, stop the send thread as well
        IS_CLIENT_CONNECTED = False
        thread_should_run = False  # Stop the send thread
        if send_thread.is_alive():
            send_thread.join()

        print(f"[INFO] Client {client_address} disconnected. Waiting for new clients...")
"""

main()