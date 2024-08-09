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
def communicate(client: socket):
    """
    Realiza um loop que fica constantemente esperando e recebendo dados
    do cliente conectado e mandando respostas de volta para ele.

    Se o cliente fechar, desligar ou por algum motivo o recebimento der erro,
    esta função fará com que o socket excluirá os dados deste cliente e
    encerrará sua conexão com ele, parando, assim o loop.
    """

    # Pega o endereço deste cliente para acesso no dicionário de conexões.
    address = client.getpeername()

    print("Nova conexão de: " + str(address))
    
    # Pega os dados deste cliente no dicionário de conexões.
    connection = connections[address]

    while True:
        data = None

        try:
            # Espera e recebe dados enviados pelo cliente.
            data = client.recv(1024)
        except:
            break

        # Se o cliente fechou seu socket, para a conexão.
        if not data: break

        client_input = data.decode()

        connection["data"] = handle_command(client_input, connection["data"], client, connections)

    print("Conexão com " + str(address) + " perdida.")

    # Remove os dados deste cliente do dicionário de conexões.
    del connections[address]
    # Fecha o socket deste cliente.
    client.close()

def accept_connections(server: socket) -> None:
    """
    Permanece em um loop que aguarda por e estabelece conexões com
    clientes.

    As novas conexões ocasionam a criação de um novo campo no dicionário
    connections que serve para guardar dados gerados por este cliente.

    Além disso, quando uma nova conexão é estabelecida, uma nova thread é
    criada para lidar com o fluxo de informações entre servidor e cliente.

    Se o servidor for fechado, ou acontecer algum erro no estabelecimento
    de conexões, o loop se encerra.
    """

    while True:
        client_socket = None
        address = None

        try:
            # Espera por uma nova conexão de cliente.
            client_socket, address = server.accept()
        except:
            return

        # Cria uma nova thread que lidará com a comunicação com o novo cliente.
        thread = Thread(target=communicate, args=(client_socket,))
        
        connections[address] = create_connection(client_socket)

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
