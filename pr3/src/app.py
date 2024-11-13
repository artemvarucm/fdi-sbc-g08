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
        self.conocimiento = Knowledge(knowledge_path)
        self.querySolver = QuerySolver()
        self.graphDrawer = GraphDrawer()
        self.lastQueryResult = None

    def query(self, queryStr):
        self.lastQueryResult = self.querySolver.query(
            queryStr,
            self.conocimiento,
        )

        print(
            tabulate(
                self.lastQueryResult, headers="keys", tablefmt="psql", showindex=False
            )
        )

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        try:
            if query == "help":
                self.help()
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
            elif "draw" in query:  # visualizacion de la ultima consulta realizada
                imagen = query.split(" ")[1].replace('"', "")
                self.graphDrawer.draw(self.lastQueryResult, imagen)
                print(f'Exportando grafo a "{imagen}"')
            elif query == "equivalente":
                print("l")
            elif "select" in query:
                self.query(query)
            else:
                print(f'COMANDO "{query}" DESCONOCIDO')
        except Exception as e:
            print(e)

    def help(self):
        print(f"{"load <base_conocimiento>":24} - añadir base de conocimiento")
        print(
            f"{"add <afirmacion>":24} - añadir una afirmacion a la base de conocimiento"
        )
        print(f"{"save":24} - guardar la base de conocimiento en archivo .ttl")
        print(
            f"{"draw <imagen>":24} - muestra la última consulta con grafos. Guarda la imagen"
        )
        print(f"{"help":24} - muestra los comandos del programa")
        print(f"{"quit":24} - salir del programa")
        print()
