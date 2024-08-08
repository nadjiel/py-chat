from argparse import ArgumentParser
import socket

def help(command: str, data: dict, client: socket, connections: dict) -> dict:
    return data

def nick(command: str, data: dict, client: socket, connections: dict) -> dict:
    command_parts = command.split()

    command_parts_len = len(command_parts)

    if command_parts_len < 2:
        client.send("O comando !nick precisa de um nome como argumento.".encode())
        return data
    
    new_nick = command_parts[1]
    
    updated_data = data.copy()
    updated_data["nick"] = new_nick

    return users(command, data, client, connections)

def users(command: str, data: dict, client: socket, connections: dict) -> dict:
    total_connections = len(connections)
    response: str = "!users " + str(total_connections)

    for connection_address in connections:
        response += " " + connections[connection_address]["data"]["nick"]
    
    client.send(response.encode())

    return data

def sendmsg(command: str, data: dict, client: socket, connections: dict) -> dict:
    return data

def msg(command: str, data: dict, client: socket, connections: dict) -> dict:
    return data

commands = {
    "!help": help,
    "!nick": nick,
    "!users": users,
    "!sendmsg": sendmsg,
    "!msg": msg,
}

def get_args():
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

def is_command(msg: str) -> bool:
    return msg.startswith('!')

def extract_prefix(command: str) -> str:
    return command.split(None, 1)[0]

def is_valid_command(command: str) -> bool:
    prefix = extract_prefix(command)

    if prefix in commands.keys(): return True

    return False

def handle_command(command: str, data: dict, client: socket, connections: dict):
    response = ""
    
    if not is_valid_command(command):
        response = command + " não é um comando válido, use o comando !help para ajuda."
        client.send(response.encode())
        return data

    prefix = extract_prefix(command)

    return commands[prefix](command, data, client, connections)
