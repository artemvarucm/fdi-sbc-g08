from knowledge import Knowledge
from query_solver import QuerySolver
from graph_drawer import GraphDrawer
from tabulate import tabulate
import re
import sys
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
        self.lastQueryResult = None

    def query(self, queryStr):
        """
        Consulta a la base de conocimiento
        """
        self.lastQueryResult = self.querySolver.query(
            queryStr,
            self.conocimiento,
        )

        print(f"Filas encontradas: {self.lastQueryResult.shape[0]}")
        print(
            tabulate(
                self.lastQueryResult.replace(pd.NA, None),
                headers="keys",
                tablefmt="psql",
                showindex=False,
                missingval="?",
            )
        )

    def load(self, query):
        """
        Carga la base de conocimiento
        """
        match = re.search(r"^load\s([\S]+)", query)
        knowledge_path = match.groups()[0]
        self.conocimiento.load(knowledge_path)

    def add(self, query):
        """
        Añade la afirmacion a la base de conocimiento
        """
        match = re.search(r"^add\b(.* \.)", query)
        afirmacion = match.groups()[0]
        self.conocimiento.importFromRaw(afirmacion)

        return

    def save(self, query):
        """
        Guarda la base de conocimiento vigente en un archivo .ttl
        """
        match = re.search(r"^save\s\"(.+)\"", query)
        knowledge_path = match.groups()[0]
        try:
            print(f'Guardando "{knowledge_path}"... ', end="")
            self.conocimiento.save(knowledge_path)
            print("OK!")
        except Exception as e:
            print(e)

    def draw(self, query):
        """
        Dibuja un grafo sobre la última consulta realizada.
        Además, guarda la imagen en el path <image_path>
        """
        match = re.search(r"^draw\s\"(.+)\"", query)
        image_path = match.groups()[0]
        try:
            print(f'Exportando grafo a "{image_path}"... ', end="")
            self.graphDrawer.draw(self.lastQueryResult, image_path)
            print("OK!")
        except Exception as e:
            print(e)


    def extractCommand(self, query):
        """
        Clasifica el comando query
        """
        query = query.lstrip()
        command = None
        if "help" == query:
            command = "help"
        elif "quit" == query:
            command = "quit"
        elif re.search(r"^load\s([\w\.]+)$", query):
            command = "load"
        elif re.search(r"^add\b", query):
            command = "add"
        elif re.search(r"^save\s\"([\w\.]+)\"$", query):
            command = "save"
        elif re.search(r"^draw\s\"([\w\.]+)\"$", query):
            command = "draw"
        elif re.search(r"^select\b", query):
            command = "select"

        return command


    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        comandoReconocido = True
        leerMasLineas = False

        query = query.lstrip()  # para detectar "select "
        command = self.extractCommand(query)

        if command is None:
            comandoReconocido = False
        if "help" == command:
            self.help()
        elif "quit" == command:
            sys.exit(1)
        elif "load" == command:  # cargar base de conocimiento
            self.load(query)
        elif "add" == command:  # añadir nueva afirmación base conocimiento
            try:
                self.add(query)
            except Exception:
                leerMasLineas = True
        elif "save" == command:  # guardar base de conocimiento
            self.save(query)
        elif "draw" == command:  # visualizacion de la ultima consulta realizad
            self.draw(query)
        elif "select" == command:
            try:
                self.query(query)
            except Exception:
                leerMasLineas = True

        if not comandoReconocido:
            print(f"COMANDO DESCONOCIDO. REVISE LA SINTAXIS.")

        return leerMasLineas

    def help(self):
        print(
            f"{"load <base_conocimiento>":28} - añadir base de conocimiento desde el archivo <base_conocimiento>"
        )
        print(
            f"{"add <afirmacion>":28} - añadir una afirmacion a la base de conocimiento"
        )
        print(
            f"{"save \"<base_conocimiento>\"":28} - guardar la base de conocimiento en el archivo <base_conocimiento>"
        )
        print(
            f"{"draw \"<imagen>\"":28} - muestra la última consulta con grafos. Guarda el png en el archivo <imagen>"
        )
        print(
            f"{"select <consulta>":28} - devuelve en formato tabla el resultado de la consulta"
        )
        print(f"{"help":28} - muestra los comandos del programa")
        print(f"{"quit":28} - salir del programa")
        print(
            f"{"Ctrl+C":28} - salir del programa o salir del modo multilinea (select, add)"
        )
        print()
