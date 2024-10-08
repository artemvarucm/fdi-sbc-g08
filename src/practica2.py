'''
Sistema basado en reglas capaz de realizar razonamiento
hacia atrás (backward chaining), incorporando lógica difusa

Recibe como parametro el archivo de base de conocimiento
'''

import argparse

from engine import Engine

parser = argparse.ArgumentParser(description="Sistema basado en reglas capaz de realizar razonamiento hacia atrás (backward chaining), incorporando lógica difusa")

# Argumento obligatorio - ruta del base de conocimiento
parser.add_argument('wisdom', help="Ruta del archivo de la base de conocimiento")
args = parser.parse_args()

with open(args.wisdom, "r", newline="\n") as f:
    # eliminamos las lineas vacias y las que empiecen por "#"
    lineas = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")] 

engine = Engine(lineas)

while True:
    query = input("> ")
    
    if (query == "print"): # mostrar por pantalla la base de conocimiento
        engine.print()
    elif (query.endswith("?")): # mostrar el valor de un hecho 
        print(engine.backward_chain(query[:-1]))