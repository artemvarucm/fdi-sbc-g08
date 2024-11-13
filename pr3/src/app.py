from knowledge import Knowledge
from query_solver import QuerySolver
from graph_drawer import GraphDrawer
import pandas as pd
from tabulate import tabulate


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path):
        self.conocimiento = Knowledge()
        self.load(knowledge_path)

        self.querySolver = QuerySolver()
        self.graphDrawer = GraphDrawer()
        self.lastQueryResult = None

    def query(self, queryStr):
        self.lastQueryResult = self.querySolver.query(
            queryStr,
            self.conocimiento,
        )

        print(f"Filas encontradas: {self.lastQueryResult.shape[0]}")
        print(
            tabulate(
                self.lastQueryResult, headers="keys", tablefmt="psql", showindex=False
            )
        )

    def load(self, knowledge_path):
        print(f'Cargando "{knowledge_path}"... ', end="")
        self.conocimiento.load(knowledge_path)
        print("OK!")

    def add(self, afirmacion):
        print(f'Añadiendo afirmación "{afirmacion}"... ', end="")
        self.conocimiento.processSubjects(afirmacion)
        print("OK!")

    def save(self, knowledge_path):
        print(f'Guardando "{knowledge_path}"... ', end="")
        self.conocimiento.save(knowledge_path)
        print("OK!")

    def draw(self, image_path):
        print(f'Exportando grafo a "{image_path}"... ', end="")
        self.graphDrawer.draw(self.lastQueryResult, image_path)
        print("OK!")

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        if query == "help":
            self.help()
        elif "load" in query:  # cargar base de conocimiento
            base_nueva = query.split(" ")[1]
            self.load(base_nueva)
        elif "add" in query:  # añadir nueva afirmación base conocimiento
            afirmacion = [query[4:]]
            self.add(afirmacion)
        elif "save" in query:  # guardar base de conocimiento
            base_nueva = query.split(" ")[1].replace('"', "")
            self.save(base_nueva)
        elif "draw" in query:  # visualizacion de la ultima consulta realizada
            image_path = query.split(" ")[1].replace('"', "")
            self.draw(image_path)
        elif query == "equivalente":
            print("l")
        elif "select" in query:
            self.query(query)
        else:
            print(f'COMANDO "{query}" DESCONOCIDO')

    def help(self):
        print(f"{"load <base_conocimiento>":24} - añadir base de conocimiento desde el archivo <base_conocimiento>")
        print(
            f"{"add <afirmacion>":24} - añadir una afirmacion a la base de conocimiento"
        )
        print(
            f"{"save <base_conocimiento>":24} - guardar la base de conocimiento en el archivo <base_conocimiento>"
        )
        print(
            f"{"draw <imagen>":24} - muestra la última consulta con grafos. Guarda el png en el archivo <imagen>"
        )
        print(f"{"help":24} - muestra los comandos del programa")
        print(f"{"quit":24} - salir del programa")
        print()
