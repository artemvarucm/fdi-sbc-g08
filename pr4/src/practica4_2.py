import click
from app import App


@click.command()
@click.argument("base_conocimiento", type=click.Path(exists=True))
def main(base_conocimiento):
    """
    Asistente virtual con ollama por debajo
    """
    app = App(base_conocimiento)
    while True:
        try:
            query = input("> ")
            app.processCommand(query)
        except Exception as e:
            print("[ERROR DURANTE EJECUCION]:", e)


if __name__ == "__main__":
    main()
