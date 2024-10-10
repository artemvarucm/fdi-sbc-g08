from engine import Engine
from config import Config


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, base_conocimiento):
        self.config = Config()

        # Inicializa el engine
        try:
            base = self.readFile(base_conocimiento)
            self.engine = Engine(
                base,
                self.config.getConfigOrDefault(["algorithm", "evaluation"], "min/max"),
            )
        except Exception:
            raise Exception(
                "Se produjo un error al intentar cargar base de conocimiento. Revise nombre del archivo."
            )

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """

        if query == "help":
            self.help()
        elif query == "print":  # mostrar por pantalla la base de conocimiento
            self.engine.print()
        elif query.endswith("?"):  # mostrar el valor de un hecho
            goals = [query[:-1]]
            showAppliedChain = self.config.getConfigOrDefault(
                ["output", "showAppliedChain"], "yes"
            )
            grado = self.engine.backward_chain(goals, showAppliedChain == "yes")
            print()
            self.evaluar(grado)
        elif query.startswith("add "):  # añadir hecho
            self.engine.newFact(query[4:])
        else:
            print(f'COMANDO "{query}" DESCONOCIDO')

    def evaluar(self, score):
        """
        Muestra por pantalla una salida formateada del grado de verdad
        """
        evalFunc = self.config.getConfigOrDefault(
            ["output", "rangeEval"],
            {
                "=1 -> Si, segurisimo",
                ">0.9 -> Si, seguro",
                ">0.5 -> Si",
                "<0.1 -> No, seguro",
                "default -> No",
            },
        )

        match = False
        default = ""
        for item in evalFunc:
            key, val = item.split(" -> ")
            if key != "default":
                op, threshold = key[:1], float(key[1:])
                if (
                    (op == "=" and threshold == score)
                    or (op == ">" and score > threshold)
                    or (op == "<" and score < threshold)
                ):
                    # Aplicando la funcion de evaluacion si cumple, IMPORTA EL ORDEN
                    match = True
                    print(val, end=" ")

                    break
            else:
                default = val

        if not match and default != "":
            print(default, end=" ")

        print(f"[{score}]")

    def help(self):
        """Muestra los comandos del programa"""

        lang = self.config.getConfigOrDefault(["output", "language"], "es")
        if lang == "es":
            self.helpEspañol()
        else:
            self.helpIngles()

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
