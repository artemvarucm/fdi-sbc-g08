from knowledge import Knowledge
from query_solver import QuerySolver

class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path):
        self.conocimiento = Knowledge(knowledge_path)
        self.querySolver = QuerySolver()
        self.querySolver.query(self.conocimiento)

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
