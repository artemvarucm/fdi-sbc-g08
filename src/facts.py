class Facts:
    """
    Estructura de datos para almacenar los
    hechos con sus respectivos grados de verdad
    """

    def __init__(self):
        self.container = {}

    def print(self):
        for key, val in self.container.items():
            print(f"{key} [{val}]")

    def addFact(self, fact, prob):
        """
        Añade información sobre el hecho
        """
        if self.contains(fact):
            raise Exception(f"Hecho {fact} ya añadido.")
        self.container[fact] = prob

    def updateFact(self, fact, prob):
        """
        Actualiza información sobre el hecho
        """
        if not self.contains(fact):
            raise Exception(f"Hecho {fact} no existe.")
        self.container[fact] = prob

    def addOrUpdateFact(self, fact, prob):
        if self.contains(fact):
            self.updateFact(fact, prob)
        else:
            self.addFact(fact, prob)

    def contains(self, fact):
        """
        Devuelve true si un hecho tiene grado de verdad mayor que 0
        """
        return (fact in self.container) and (self.container[fact] > 0)

    def getValorVerdad(self, fact):
        """
        Devuelve el grado de verdad de un hecho
        """
        if fact in self.container:
            return self.container[fact]

        return 0
