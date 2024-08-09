import socket
from args import get_args
from threading import Thread

from args import handle_command

connections = {}

def close_connections() -> None:
    for address in connections:
        connections[address]["socket"].close()

def create_connection(thread: Thread, socket: socket) -> dict:
    """
    Cria um dicionário representando a conexão de um cliente.

    O dicionário tem os atributos thread e data que contêm,
    respectivamente, a thread que está responsável por essa
    conexão e um dicionário com os dados desse cliente.
    """

    return {
        "thread": thread,
        "socket": socket,
        "data": {
            "nick": "",
            "requests": 0,
            "stopped": False
        },
    }

def communicate(client: socket, address):
    print("Nova conexão de: " + str(address))

    connection = connections[address]

    while not connection["data"]["stopped"]:
        data = None

        try:
            data = client.recv(1024)
        except:
            break

        if not data: break

        client_input = data.decode()

        connection["data"] = handle_command(client_input, connection["data"], client, connections)

    del connections[address]
    client.close()

def start(host: str, port: int):
    server = socket.socket()

    server.bind((host, port))
    server.listen()

    while True:
        client_socket, address = server.accept()

        # print("address: ")
        # print(address)
        # print("sockname: ")
        # print(client_socket.getsockname())
        # print("peername: ")
        # print(client_socket.getpeername())

        thread = Thread(target=communicate, args=(client_socket, address))
        thread.start()

        connections[address] = create_connection(thread, client_socket)
        #print(connections)
        # connections.append(create_connection(thread))

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
    #print(args)
    # print(socket.gethostname())
    start(args.host, args.port)
