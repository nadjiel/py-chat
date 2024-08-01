import socket
from args import get_args

def start(host: str, port: int):
    server_socket = socket.socket()

    server_socket.bind((host, port))
    server_socket.listen()

    client_socket, address = server_socket.accept()
    print(client_socket)
    print(address)

    print("New connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = client_socket.recv(1024).decode()

        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        data = input(' -> ')
        client_socket.send(data.encode())  # send data to the client

    client_socket.close()  # close the connection


if __name__ == '__main__':
    args = get_args()
    print(args)
    # print(socket.gethostname())
    start(args.host, args.port)
