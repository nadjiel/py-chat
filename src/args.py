from argparse import ArgumentParser
import socket

def get_args():
    """
    Utiliza o argparse para retornar os argumentos do programa.

    Os argumentos definidos aqui são o host (-a, --address) e a
    port (-p, --port).
    Inicialmente eles são definidos para localhost e 5000, respectivamente.
    """
    
    parser = ArgumentParser()

    parser.add_argument(
        "-a", "--address",
        dest="host",
        default="localhost",
        help="O endereço no qual este servidor deve rodar"
    )
    parser.add_argument(
        "-p", "--port",
        default=5000,
        help="A porta na qual este servidor deve rodar",
        type=int
    )

    return parser.parse_args()

def broadcast(message: str, connections: dict, exclude: tuple = ()) -> None:
    for address in connections:
        if address in exclude: continue

        connections[address]["socket"].send(message.encode())

def help(command: str, client_address, connections: dict) -> dict:
    # Pega os dados necessários do dicionário de conexões.
    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    response: str = ""

    commands_amount = len(commands)
    counter = 0

    for command in commands:
        counter += 1

        response += command + ": " + commands[command]["help"] + ";"

        if counter < commands_amount: response += "\n"
    
    # Manda a ajuda para o cliente.
    client.send(response.encode())
    
    return data

def nick(command: str, client_address, connections: dict) -> dict:
    # Pega os dados necessários do dicionário de conexões.
    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    response: str = ""

    command_parts = command.split()

    command_parts_length = len(command_parts)

    # Valida o comando.
    if command_parts_length < 2:
        response = "O comando !nick precisa de um nome como argumento."

        client.send(response.encode())
        return data
    if command_parts_length > 2:
        response = "O comando !nick só recebe um nome como argumento."

        client.send(response.encode())
        return data
    
    new_nick = command_parts[1]
    
    data["nick"] = new_nick

    # Chama o comando users para que o usuário receba sua mensagem.
    return users(command, client_address, connections)

def changenickname(command: str, client_address, connections: dict) -> dict:
    # Pega os dados necessários do dicionário de conexões.
    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    response: str = ""

    command_parts = command.split()

    command_parts_length = len(command_parts)

    # Valida o comando.
    if command_parts_length < 2:
        response = "O comando !changenickname precisa de um nome como argumento."

        client.send(response.encode())
        return data
    if command_parts_length > 2:
        response = "O comando !changenickname só recebe um nome como argumento."

        client.send(response.encode())
        return data
    
    old_nick = data["nick"]
    new_nick = command_parts[1]
    
    data["nick"] = new_nick

    response = "!changenickname " + old_nick + " " + new_nick

    # Manda para todos os clientes conectados a notícia da atualização.
    broadcast(response, connections)

    return data

def users(command: str, client_address, connections: dict) -> dict:
    # Pega os dados necessários do dicionário de conexões.
    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    total_connections = len(connections)

    response: str = "!users " + str(total_connections)

    for connection_address in connections:
        response += " " + connections[connection_address]["data"]["nick"]
    
    # Manda os usuário conectados para o cliente.
    client.send(response.encode())

    return data

def sendmsg(command: str, client_address, connections: dict) -> dict:
    # Pega os dados necessários do dicionário de conexões.
    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    response = ""

    command_parts = command.split(None, 1)

    command_parts_length = len(command_parts)

    # Valida o comando.
    if command_parts_length < 2:
        response = "O comando !sendmsg precisa de uma mensagem como argumento."

        client.send(response.encode())
        return data
    
    sender: str = data["nick"]

    response: str = (
        "!msg " +
        sender + " " +
        command_parts[1]
    )

    # Manda para todos os clientes conectados menos este a mensagem recebida.
    broadcast(response, connections, exclude=(client_address,))
    
    return data

def poke(command: str, client_address, connections: dict) -> dict:
    # Pega os dados necessários do dicionário de conexões.
    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    response: str = ""

    command_parts = command.split()

    command_parts_length = len(command_parts)

    # Valida o comando.
    if command_parts_length < 2:
        response = "O comando !poke precisa de um nome como argumento."

        client.send(response.encode())
        return data
    if command_parts > 2:
        response = "O comando !poke só recebe o nome de quem vai ser cutucado."

        client.send(response.encode())
        return data
    
    poker = data["nick"]
    poked = command_parts[1]

    response = "!poke " + poker + " " + poked

    # Manda para todos os clientes conectados a mensagem de poke.
    broadcast(response, connections)

    return data

commands = {
    "!help": {
        "command": help,
        "help": "Retorna informações sobre os comandos disponíveis"
    },
    "!nick": {
        "command": nick,
        "help": "Guarda o seu nickname no servidor"
    },
    "!changenickname": {
        "command": changenickname,
        "help": "Atualiza seu nickname e avisa a todos conectados sobre isso"
    },
    "!users": {
        "command": users,
        "help": "Retorna informações sobre os usuários conectados"
    },
    "!sendmsg": {
        "command": sendmsg,
        "help": "Envia uma mensagem no chat para todos verem"
    },
    "!poke": {
        "command": poke,
        "help": "Cutuca alguém e avisa a todos sobre isso"
    },
}

def extract_prefix(command: str) -> str:
    """
    Retorna a primeira palavra da string do comando
    (!nick, !help, !changenickname, por exemplo)
    """

    return command.split(None, 1)[0]

def command_is_valid(command: str) -> bool:
    """
    Diz se a string de comando passada é um dos comandos
    disponíveis.
    """
    
    prefix = extract_prefix(command)

    if prefix in commands.keys(): return True

    return False

def handle_command(command: str, client_address, connections: dict):
    """
    Avalia se o usuário mandou um comando válido e, se sim,
    executa o que este comando deve executar e retorna os dados
    do usuário atualizados.

    Se for o primeiro request deste usuário, ele só pode mandar
    !nick ou !help como comandos.
    """

    connection = connections[client_address]
    client = connection["socket"]
    data = connection["data"]

    response = ""
    
    if not command_is_valid(command):
        response = command + " não é um comando válido, use o comando !help para ajuda."

        client.send(response.encode())
        return data

    prefix = extract_prefix(command)

    # Se é o primeiro request deste usuário ele deve obrigatoriamente
    # ser !nick ou !help
    if data["requests"] == 0:
        if prefix != "!nick" and prefix != "!help":
            client.close()
            return data

    # Incrementa o número de requests deste usuário
    data["requests"] += 1

    # Executa o comando determinado e retorna os dados que ele
    # atualiza (ou não atualiza)
    return commands[prefix]["command"](command, client_address, connections)
