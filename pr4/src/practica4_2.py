import click
from app import App


@click.command()
@click.argument("bases_dir", type=click.Path(exists=True))
def main(bases_dir):
    """
    Asistente virtual con ollama por debajo
    """
    app = App(bases_dir)
    while True:
        try:
            query = input("> ")
            app.processCommand(query)
        except Exception as e:
            print("[ERROR DURANTE EJECUCION]:", e)


if __name__ == "__main__":
    main()
