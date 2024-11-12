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

    def query(self, queryStr):
        print(
            self.querySolver.query(
                """
                               select ?pers, ?relig
                               where { 
                                ?pers wdt:P31 q8:persona .
                                ?pers t8:religion ?relig .
                               }
                               """,
                self.conocimiento,
            )
        )

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        if query == "help":
            self.helpEspañol()
        elif "load" in query:  # cargar base de conocimiento
            print(query.split(" ")[1])
            self.conocimiento.load(query.split(" ")[1])
        elif "add" in query:   # añadir nueva afirmación base conocimiento
            self.conocimiento.processSubjects([query[4:]])
        elif query == "save":  # guardar base de conocimiento
            print("l")
        elif query == "draw":  # visualizacion de la ultima consulta realizada 
            print("l")
        elif query == "equivalente":
            print("l")
        else:
            print(f'COMANDO "{query}" DESCONOCIDO')

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
