import socket


def start_client(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    print("CONNECTED TO SERVER")
    print("You can close the connection anytime by typing '-q' and then enter.")

    message = input(">>> ")
    while message != "-q":
        client_socket.send(message.encode('utf-8'))
        message = input(">>> ")

    client_socket.close()
