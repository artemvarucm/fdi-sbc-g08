from hornyClause import HornClause


class BaseReglas:
    """
    Contenedor de varias HornClause.

    Internamente es un diccionario que tiene:
    - El consecuente como llave
    - Lista de clausulas con ese consecuente como valor
    """

    def __init__(self):
        self.container = {}

    def addFromString(self, reglaStr):
        """
        Añade una clausula a partir de una cadena de caracteres
        """

        clause = HornClause(reglaStr)
        key = clause.getConsecuente()
        if key not in self.container:
            self.container[key] = []

        self.container[key].append(clause)

    def findByConsecuente(self, consecuente):
        """
        Devuelve la lista de clausulas dado un consecuente
        """

        if consecuente not in self.container:
            return []

        return self.container[consecuente]

    def print(self):
        """
        Muestra las clausulas de la base
        """

        for consecuente in self.container:
            for r in self.container[consecuente]:
                r.print()
