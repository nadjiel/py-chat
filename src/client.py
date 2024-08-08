import socket
from args import get_args

def start(host: str, port: int):
    # Instancia o socket
    client_socket = socket.socket()
    # Conecta ao servidor neste host e porta
    client_socket.connect((host, port))

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        # Envia a mensagem em lowercase e sem espaços nas pontas
        client_socket.send(message.encode())

        # Recebe a resposta do servidor
        data = client_socket.recv(1024)

        if not data: break

        server_output = data.decode()

        print(server_output)

        message = input(" -> ")

    # Fecha a conexão com o servidor
    client_socket.close()


if __name__ == '__main__':
    args = get_args()
    #print(args)
    start(args.host, args.port)
