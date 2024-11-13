import argparse
import sys
from app import App
import click


@click.command()
@click.argument("base_conocimiento", type=click.Path(exists=True))
@click.option(
    "--script",
    type=click.Path(exists=True),
    help="Ruta del script con las instrucciones",
)
def main(base_conocimiento, script):
    """
    Programa que permite representar y consultar redes semánticas
    usando un subconjunto simplificado de RDF y SPARQL partiendo de la base de conocimiento
    """
    try:
        app = App(base_conocimiento)
    except Exception as e:
        # Salimos en caso de fallo de carga del archivo
        print("[ERROR]:", e)
        sys.exit(1)

    # Bucle principal del programa
    multiLine = False
    while True:
        if multiLine:
            try:
                query += " " + input("  ")
            except KeyboardInterrupt:  # si pulsa Ctrl+C -> salimos del modo multilinea
                query = input("\n> ")

        else:
            query = input("> ")

        try:
            if query == "quit":
                sys.exit(1)
            multiLine = app.processCommand(query)
        except Exception as e:
            print("[ERROR DURANTE EJECUCION]:", e)


if __name__ == "__main__":
    main()
