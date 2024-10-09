import toml
import utils
from engine import Engine

class App:
    def __init__(self, base_conocimiento):
        self.loadToml()

        # Inicializa el engine
        self.engine = Engine(utils.readFile(base_conocimiento))

    def processCommand(self, query):
        if query == "help":
            self.help()
        elif query == "print":  # mostrar por pantalla la base de conocimiento
            self.engine.print()
        elif query.endswith("?"):  # mostrar el valor de un hecho
            goals = [query[:-1]]
            self.engine.evaluar(self.engine.backward_chain(goals))
        elif query.startswith("add "):  # añadir hecho
            self.engine.newFact(query[4:])
        else:
            print(f'COMANDO "{query}" DESCONOCIDO')

    def loadToml(self):
        try:
            with open("config.toml", "r") as f:
                self.config = toml.load(f)
        except Exception:
            print(
                "Archivo config.toml no se puedo cargar. Usando configuración predeterminada."
            )

    def help(self):
        lang = self.config["output"]["language"]
        if lang == "es":
            self.helpEspañol()
        else:
            self.helpIngles()

    def helpEspañol(self):
        """Muestra los comandos del programa"""

        print(f"{"print":22} - mostrar por pantalla la base de conocimiento")
        print(f"{"add <hecho>":22} - añadir un hecho con grado de verdad 1")
        print(f"{"add <hecho> [<grado>]":22} - añadir un hecho con un grado de verdad")
        print(f"{"<hecho>?":22} - devuelve el grado de verdad del hecho")
        print(f"{"help":22} - muestra los comandos del programa")
        print(f"{"quit":22} - salir del programa")
        print()

    def helpIngles(self):
        """Muestra los comandos del programa"""

        print(f"{"print":22} - display knowledge base")
        print(f"{"add <fact>":22} - add fact with truth score equal to 1")
        print(f"{"add <fact> [<score>]":22} - add fact with truth score")
        print(f"{"<fact>?":22} - return truth score")
        print(f"{"help":22} - display available commands")
        print(f"{"quit":22} - quit program")
        print()
