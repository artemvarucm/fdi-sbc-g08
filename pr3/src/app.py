from knowledge import Knowledge
from query_solver import QuerySolver
from graph_drawer import GraphDrawer
import pandas as pd


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path):
        self.conocimiento = Knowledge(knowledge_path)
        self.querySolver = QuerySolver()
        self.graphDrawer = GraphDrawer()

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
        try:
            if query == "help":
                self.helpEspañol()
            elif "load" in query:  # cargar base de conocimiento
                base_nueva = query.split(" ")[1]
                self.conocimiento.load(base_nueva)
                print(f'Cargando "{base_nueva}"')
            elif "add" in query:  # añadir nueva afirmación base conocimiento
                afirmacion = [query[4:]]
                self.conocimiento.processSubjects(afirmacion)
                print(f'Añadiendo afirmación "{afirmacion}"')
            elif "save" in query:  # guardar base de conocimiento
                base_nueva = query.split(" ")[1]
                self.conocimiento.save(base_nueva)
                print(f'Guardando "{base_nueva}"')
            elif query == "draw":  # visualizacion de la ultima consulta realizada
                imagen = query.split(" ")[1]
                self.graphDrawer.draw(
                    pd.DataFrame({"A": [1, 2, 3], "B": [2, 5, 5], "C": [0, 8, 7]})
                )
                print(f'Exportando grafo a "{imagen}"')
            elif query == "equivalente":
                print("l")
            elif "select" in query:
                print("l")
            else:
                print(f'COMANDO "{query}" DESCONOCIDO')
        except Exception as e:
            print(e)

    def help(self):
        print(f"{"load <base_conocimiento>":22} - añadir base de conocimiento")
        print(
            f"{"add <afirmacion>":22} - añadir una afirmacion a la base de conocimiento"
        )
        print(f"{"save":22} - guardar la base de conocimiento en archivo .ttl")
        print(
            f"{"draw <imagen>":22} - muestra la última consulta con grafos. Guarda la imagen"
        )
        print(f"{"help":22} - muestra los comandos del programa")
        print(f"{"quit":22} - salir del programa")
        print()
