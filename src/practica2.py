'''
Sistema basado en reglas capaz de realizar razonamiento
hacia atrás (backward chaining), incorporando lógica difusa

Recibe como parametro el archivo de base de conocimiento
'''

import argparse

parser = argparse.ArgumentParser(description="Sistema basado en reglas capaz de realizar razonamiento hacia atrás (backward chaining), incorporando lógica difusa")
# Obligatorios
parser.add_argument('base_conocimiento', required=True, help="Ruta del archivo de la base de conocimiento")
args = parser.parse_args()

with open(args[0], "r", newline="\n") as f:
    lineas = [line.rstrip() for line in f]

reglas = lineas[lineas.index('## Trabajos') + 1:lineas.index('## Habilidades')]
habilidades = lineas[lineas.index('## Habilidades') + 1:]

print(f"reglas {reglas}")
print(f"habilidades {habilidades}")


