class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    """def __init__(self, base_conocimiento):
        self.config = Config()

        # Inicializa el engine
        try:
            base = self.readFile(base_conocimiento)
            self.engine = Engine(
                base,
                self.config.getConfigOrDefault(["algorithm", "evaluation"], "min/max"),
            )
        except FileNotFoundError:
            raise Exception("Archivo " + base_conocimiento + " no encontrado.")
"""

    def readFile(self, file_path):
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

    def helpEspañol(self):
        print(f"{"print":22} - mostrar por pantalla la base de conocimiento")
        print(f"{"add <hecho>":22} - añadir un hecho con grado de verdad 1")
        print(f"{"add <hecho> [<grado>]":22} - añadir un hecho con un grado de verdad")
        print(f"{"<hecho>?":22} - devuelve el grado de verdad del hecho")
        print(f"{"help":22} - muestra los comandos del programa")
        print(f"{"quit":22} - salir del programa")
        print()

    def helpIngles(self):
        print(f"{"print":22} - display knowledge base")
        print(f"{"add <fact>":22} - add fact with truth score equal to 1")
        print(f"{"add <fact> [<score>]":22} - add fact with truth score")
        print(f"{"<fact>?":22} - return truth score")
        print(f"{"help":22} - display available commands")
        print(f"{"quit":22} - quit program")
        print()
