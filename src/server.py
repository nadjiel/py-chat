import socket
from args import get_args
from threading import Thread

connections = []
threads = []

def communicate(client: socket, address):
    print("New connection from: " + str(address))
    print("socket:")
    print(client)

    while True:
        data = client.recv(1024).decode()

        if not data: break
        
        print("from connected user: " + str(data))
        data = input(' -> ')
        client.send(data.encode())  # send data to the client

    client.close()

def start(host: str, port: int):
    server_socket = socket.socket()

    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        client_socket, address = server_socket.accept()

        thread = Thread(target=communicate, args=(client_socket, address))
        thread.start()
        threads.append(thread)

        # thread.join()
    
    # print(client_socket)
    # print(address)

    # print("New connection from: " + str(address))

    # while True:
    #     # receive data stream. it won't accept data packet greater than 1024 bytes
    #     data = client_socket.recv(1024).decode()

    #     if not data:
    #         # if data is not received break
    #         break
        
    #     print("from connected user: " + str(data))
    #     data = input(' -> ')
    #     client_socket.send(data.encode())  # send data to the client

    # client_socket.close()  # close the connection


if __name__ == '__main__':
    args = get_args()
    print(args)
    # print(socket.gethostname())
    start(args.host, args.port)
