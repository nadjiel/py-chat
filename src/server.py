import socket
from args import get_args
from threading import Thread

from args import handle_command

connections = {}
threads = []

def create_connection(thread: Thread) -> dict:
    return {
        "thread": thread,
        "data": {},
    }

def communicate(client: socket, address):
    print("Nova conexão de: " + str(address))

    connection = connections[str(address)]

    print(connection)

    while True:
        data = client.recv(1024).decode()

        if not data: break

        client_input = str(data)

        connection["data"] = handle_command(client, connection["data"], client_input)

        print(connection)
        
        # print("from connected user: " + str(data))
        # data = input(' -> ')
        # client.send(data.encode())  # send data to the client

    client.close()

def start(host: str, port: int):
    server = socket.socket()

    server.bind((host, port))
    server.listen()

    while True:
        client_socket, address = server.accept()

        thread = Thread(target=communicate, args=(client_socket, address))
        thread.start()

        connections[str(address)] = create_connection(thread)
        # connections.append(create_connection(thread))

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
