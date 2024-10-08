'''
Sistema basado en reglas capaz de realizar razonamiento
hacia atrás (backward chaining), incorporando lógica difusa

Recibe como parametro el archivo de base de conocimiento
'''

import argparse
from engine import Engine
import utils

parser = argparse.ArgumentParser(description="Sistema basado en reglas capaz de realizar razonamiento hacia atrás (backward chaining), incorporando lógica difusa")

# Argumento obligatorio - ruta del base de conocimiento
parser.add_argument('base_conocimiento', help="Ruta del archivo de la base de conocimiento")
args = parser.parse_args()

# Inicializa el engine
engine = Engine(utils.readFile(args.base_conocimiento))

# Muestra los comandos
utils.help()

# Bucle principal del programa
while True:
    query = input("> ")
    try :
        if (query == "help"):
            utils.help()
        elif (query == "print"): # mostrar por pantalla la base de conocimiento
            engine.print()
        elif (query.endswith("?")): # mostrar el valor de un hecho 
            goals = [query[:-1]]
            engine.evaluar(engine.backward_chain(goals))
        elif (query.startswith("add ")): # añadir hecho
            engine.newFact(query[4:])
        else:
            print(f"COMANDO \"{query}\" DESCONOCIDO")
    except Exception as e:
        print("[ERROR DURANTE EJECUCION]:", e)

