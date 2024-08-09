from argparse import ArgumentParser

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
