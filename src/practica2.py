import argparse
import sys
from app import App

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sistema basado en reglas capaz de realizar razonamiento hacia atrás (backward chaining), incorporando lógica difusa"
    )

    # Argumento obligatorio - ruta del base de conocimiento
    parser.add_argument(
        "base_conocimiento", help="Ruta del archivo de la base de conocimiento"
    )
    args = parser.parse_args()

    try:
        app = App(args.base_conocimiento)
    except Exception as e:
        # Salimos en caso de fallo de carga del archivo
        print("[ERROR]:", e)
        sys.exit(1)

    # Muestra los comandos
    app.help()

    # Bucle principal del programa
    while True:
        query = input("> ")
        try:
            if query == "quit":
                sys.exit(1)
            app.processCommand(query)
        except Exception as e:
            print("[ERROR DURANTE EJECUCION]:", e)
