import socket

FORMAT = "ascii"
DEST_NAME = socket.gethostname()
DEST_IP = socket.gethostbyname(DEST_NAME)
PORT = 50005
INITIAL_BYTE_SIZE = 1024
CONNECTED = True
DISCONNECT_MSG = "quit"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, PORT))
print("[CONNECTED] Client connected\n")

while CONNECTED:
    # server_response = client_socket.recv(INITIAL_BYTE_SIZE)
    # print("[CONNECTION STATUS]: ",server_response.decode())
    msg = input(f"{DEST_NAME}@{DEST_IP}:$ ") or "[EMPTY STRING]"
    client_socket.send(msg.encode(FORMAT))
    if msg != "quit":
        print("[SENT] Message sent...\n")
        server_reply = client_socket.recv(INITIAL_BYTE_SIZE).decode(FORMAT)
        print(f"[SERVER]:$ {server_reply}")
        continue
    CONNECTED = False

print(f"[SHUTDOWN] Client has shutdown...")
client_socket.close()