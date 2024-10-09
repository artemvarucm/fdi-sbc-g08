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
