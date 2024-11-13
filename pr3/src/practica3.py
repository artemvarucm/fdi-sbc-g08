import argparse
import sys
from app import App
import click
from utils import readFile


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

    try:
        multiLine = False  # juntar lineas leidas consecutivamente

        # Ejecuta el script antes de empezar
        if script is not None:
            for line in readFile(script):
                if multiLine:
                    query += " " + line
                else:
                    query = line
                multiLine = app.processCommand(query)

        # Bucle principal del programa
        multiLine = False
        while True:
            if multiLine:
                query += " " + input("  ")
            else:
                query = input("> ")
            if query.strip():  # poder hacer enter sin ejecutar nada
                multiLine = app.processCommand(query)

    except KeyboardInterrupt:
        if multiLine:  # si pulsa Ctrl+C -> salimos del modo multilinea
            print()
            multiLine = False
        else:
            sys.exit(1)
    except Exception as e:
        print("[ERROR DURANTE EJECUCION]:", e)


if __name__ == "__main__":
    main()
