import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print(f"CLIENT DISCONNECTED")
            break

        print(f'<<< {data}')

    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"CLIENT CONNECTED")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()
