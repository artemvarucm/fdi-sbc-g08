from pathlib import Path


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
        raise Exception("[ERROR]: Archivo " + file_path + " no encontrado.")

    return lineas


def addFile(file_name, file_path):
    """Añade una base de conocimiento"""
    contenido = readFile(file_path)

    with open(Path("../bases/usuario", file_name), "w", encoding="utf-8") as archivo:
        archivo.write(" ".join(contenido))
