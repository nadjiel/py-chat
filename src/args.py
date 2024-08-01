from argparse import ArgumentParser

def help(data: dict) -> dict:
    return data

def nick(data: dict) -> dict:
    return data

def users(data: dict) -> dict:
    return data

def sendmsg(data: dict) -> dict:
    return data

def msg(data: dict) -> dict:
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
        help="A porta na qual este servidor deve rodar"
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

def handle_command(data: dict, command: str):
    if not is_valid_command(command):
        print(command + " não é um comando válido, use o comando !help para ajuda.")
        return data

    prefix = extract_prefix(command)

    return commands[prefix](data)

def get_nick():
    input()
