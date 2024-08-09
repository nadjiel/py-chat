import socket
from args import get_args
from threading import Thread

from args import handle_command

command = ""
connections = {}

def close_connections() -> None:
    """
    Fecha todos os sockets de clientes armazenados no dicionário
    de conexões.
    """

    for address in connections:
        client_socket = connections[address]["socket"]
        
        client_socket.close()

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

def accept_connections(server: socket) -> None:
    welcome_msg = "Bem-vindo ao PyChat! 🐍 Se precisar de ajuda use !help."

    while command != "!exit":
        client_socket = None
        address = None

        try:
            client_socket, address = server.accept()
        except:
            return

        thread = Thread(target=communicate, args=(client_socket, address))
        
        connections[address] = create_connection(thread, client_socket)

        client_socket.send(welcome_msg.encode())

        thread.start()

def start(host: str, port: int):
    """
    Inicia o programa separando uma thread que será responsável por
    aceitar conexões de clientes, enquanto deixa a thread principal
    receber entradas do terminal para fechar o servidor quando desejado.
    """
    
    # Instancia o socket
    server = socket.socket()

    # Define o endereço e porta aos quais este socket pertence
    server.bind((host, port))
    # Prepara este socket para escutar clientes
    server.listen()

    # Separando uma thread para estabelecimento de conexões
    thread = Thread(target=accept_connections, args=(server,))
    thread.start()

    print("Esperando por conexões...")
    print("Quando quiser, use !exit para encerrar o servidor.")

    while True:
        command = input().strip()

        if command != "!exit":
            print("Comando inválido! Se quiser sair use !exit para encerrar o servidor.")
        else:
            break
    
    # Fecha os sockets dos clientes
    close_connections()
    # Fecha o socket do servidor
    server.close()


if __name__ == '__main__':
    args = get_args()
    start(args.host, args.port)
