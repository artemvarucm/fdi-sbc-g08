from excepciones import FileNotFoundException

def readFile(file_path):
    """
    Lee el fichero en file_path y devuelve las lineas del fichero
    eliminando las lineas vacias y las que comienzan por "#"
    """
    try:
        with open(file_path, "r", newline="\n") as f:
            lineas = [
                line.strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
    except FileNotFoundError:
        raise FileNotFoundException(file_path)

    return lineas
