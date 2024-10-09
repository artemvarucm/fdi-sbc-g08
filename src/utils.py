def readFile(file_path):
    """
    Lee el fichero en file_path y devuelve las lineas del fichero
    eliminando las lineas vacias y las que comienzan por "#"
    """

    with open(file_path, "r", newline="\n") as f:
        lineas = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    return lineas


def help():
    """Muestra los comandos del programa"""

    print(f"{"print":22} - mostrar por pantalla la base de conocimiento")
    print(f"{"add <hecho>":22} - añadir un hecho con grado de verdad 1")
    print(f"{"add <hecho> [<grado>]":22} - añadir un hecho con un grado de verdad")
    print(f"{"<hecho>?":22} - devuelve el grado de verdad del hecho")
    print(f"{"help":22} - muestra los comandos del programa")
    print()
