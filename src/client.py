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
    
    client.shutdown(socket.SHUT_RDWR)
    
    print("Conexão perdida, insira qualquer coisa para sair.")

def start(host: str, port: int):
    # Instancia o socket
    client_socket = socket.socket()
    # Conecta ao servidor neste host e porta
    client_socket.connect((host, port))

    thread = Thread(target=communicate, args=(client_socket,))
    thread.start()

    command = input().strip().lower()

    while command != 'bye':
        #data = None

        try:
            # Envia o comando recebido pelo terminal
            client_socket.send(command.encode())
        except:
            break

        command = input()

    # Fecha a conexão com o servidor
    client_socket.close()


if __name__ == '__main__':
    args = get_args()
    #print(args)
    start(args.host, args.port)
