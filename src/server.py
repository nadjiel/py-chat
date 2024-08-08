import socket
from args import get_args
from threading import Thread

from args import handle_command

connections = {}

def create_connection(thread: Thread) -> dict:
    """
    Cria um dicionário representando a conexão de um cliente.

    O dicionário tem os atributos thread e data que contêm,
    respectivamente, a thread que está responsável por essa
    conexão e um dicionário com os dados desse cliente.
    """

    return {
        "thread": thread,
        "data": {
            "nick": ""
        },
    }

def communicate(client: socket, address):
    print("Nova conexão de: " + str(address))

    connection = connections[str(address)]

    print(connection)

    while True:
        data = client.recv(1024).decode()

        if not data: break

        client_input = str(data)

        connection["data"] = handle_command(client_input, connection["data"], client)

        print(connection)
        
        # print("from connected user: " + str(data))
        # data = input(' -> ')
        # client.send(data.encode())  # send data to the client

    del connections[str(address)]
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
        print(connections)
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
