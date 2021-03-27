from instrumentserver.client import Client


if __name__ == "__main__":
    cli = Client()
    yoko = cli.get_instrument("YOKO")


