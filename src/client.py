import socket
from args import get_args
from threading import Thread

def communicate(client: socket) -> None:
    """
    Realiza um loop que fica constantemente esperando e recebendo dados
    do servidor conectado.

    Se o servidor fechar, desligar ou por algum motivo o recebimento der erro,
    esta função fará com que o socket cliente não mais possa se comunicar
    com o servidor.
    """
    
    while True:
        try:
            # Espera o recebimento de dados de servidor
            data = client.recv(1024)
        except:
            break

        if not data: break

        server_output = data.decode()

        print(server_output)
    
    client.close()
    
    print("Conexão perdida, pressione enter para sair.")

def start(host: str, port: int):
    """
    Ponto de entrada do código deste cliente.

    Esta função 
    """

    # Instancia o socket
    client_socket = socket.socket()
    # Conecta ao servidor neste host e porta
    client_socket.connect((host, port))

    print("Bem-vindo ao PyChat! 🐍")
    print("Quando quiser desconectar use !exit.")

    # Começa uma thread responsável por receber dados do servidor,
    # já que a principal ficará travada com entrada de dados.
    thread = Thread(target=communicate, args=(client_socket,))
    thread.start()

    while True:
        command = input().strip()

        if command == "!exit":
            break

        try:
            # Envia o comando recebido pelo terminal
            client_socket.send(command.encode())
        except:
            break

    # Fecha a conexão com o servidor
    client_socket.close()

if __name__ == '__main__':
    args = get_args()
    start(args.host, args.port)
