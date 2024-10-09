"""
Sistema basado en reglas capaz de realizar razonamiento
hacia atrás (backward chaining), incorporando lógica difusa

Recibe como parametro el archivo de base de conocimiento
"""

import argparse
from app import App

parser = argparse.ArgumentParser(
    description="Sistema basado en reglas capaz de realizar razonamiento hacia atrás (backward chaining), incorporando lógica difusa"
)

# Argumento obligatorio - ruta del base de conocimiento
parser.add_argument(
    "base_conocimiento", help="Ruta del archivo de la base de conocimiento"
)
args = parser.parse_args()

app = App(args.base_conocimiento)

# Muestra los comandos
app.help()

# Bucle principal del programa
while True:
    query = input("> ")
    try:
        if query == "quit":
            break
        app.processCommand(query)
    except Exception as e:
        print("[ERROR DURANTE EJECUCION]:", e)
