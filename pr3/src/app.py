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
        self.conocimiento = Knowledge()
        self.load(knowledge_path)

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

    def load(self, knowledge_path):
        """
        Carga la base de conocimiento
        """
        try:
            print(f'Cargando "{knowledge_path}"... ', end="")
            self.conocimiento.load(knowledge_path)
            print("OK!")
        except Exception as e:
            print(e)

    def add(self, afirmacion):
        """
        Añade la afirmacion a la base de conocimiento
        """
        self.conocimiento.importFromRaw(afirmacion)

    def save(self, knowledge_path):
        """
        Guarda la base de conocimiento vigente en un archivo .ttl
        """
        try:
            print(f'Guardando "{knowledge_path}"... ', end="")
            self.conocimiento.save(knowledge_path)
            print("OK!")
        except Exception as e:
            print(e)

    def draw(self, image_path):
        """
        Dibuja un grafo sobre la última consulta realizada.
        Además, guarda la imagen en el path <image_path>
        """
        try:
            print(f'Exportando grafo a "{image_path}"... ', end="")
            self.graphDrawer.draw(self.lastQueryResult, image_path)
            print("OK!")
        except Exception as e:
            print(e)

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        comandoReconocido = True
        leerMasLineas = False

        query = query.lstrip()  # para detectar "select "
        if "help" == query:
            self.help()
        elif "quit" == query:
            sys.exit(1)
        elif re.search(r"^load\s([\w\.]+)$", query):  # cargar base de conocimiento
            match = re.search(r"^load\s([\S]+)", query)
            base_nueva = match.groups()[0]
            self.load(base_nueva)
        elif re.search(r"^add\b", query):  # añadir nueva afirmación base conocimiento
            match = re.search(r"^add\b(.* \.)", query)
            if not match:
                leerMasLineas = True
            else:
                afirmacion = match.groups()[0]
                try:
                    self.add(afirmacion)
                except Exception:
                    leerMasLineas = True
        elif re.search(r"^save\s\"([\w\.]+)\"$", query):  # guardar base de conocimiento
            match = re.search(r"^save\s\"(.+)\"", query)
            base_nueva = match.groups()[0]
            self.save(base_nueva)
        elif re.search(
            r"^draw\s\"([\w\.]+)\"$", query
        ):  # visualizacion de la ultima consulta realizada
            match = re.search(r"^draw\s\"(.+)\"", query)
            image_path = match.groups()[0]
            self.draw(image_path)
        elif re.search(r"^select\b", query):
            try:
                self.query(query)
            except Exception:
                leerMasLineas = True
        else:
            comandoReconocido = False

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
