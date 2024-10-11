class Facts:
    """
    Estructura de datos para almacenar los
    hechos con sus respectivos grados de verdad
    """

    def __init__(self):
        self.container = {}

    def print(self):
        """
        Muestra todos los hechos con el grado de verdad
        """
        for key, val in self.container.items():
            print(f"{key} [{val}]")

    def addFact(self, fact, score):
        """
        Añade información sobre el hecho
        """
        if self.contains(fact):
            raise Exception(f"Hecho {fact} ya añadido.")
        if score > 1 or score < 0:
            raise Exception("El grado de certeza tiene que estar entre 0 y 1")
        
        self.container[fact] = score

    def updateFact(self, fact, score):
        """
        Actualiza información sobre el hecho
        """
        if not self.contains(fact):
            raise Exception(f"Hecho {fact} no existe.")
        if score > 1 or score < 0:
            raise Exception("El grado de certeza tiene que estar entre 0 y 1")
        
        self.container[fact] = score

    def addOrUpdateFact(self, fact, score):
        if self.contains(fact):
            self.updateFact(fact, score)
        else:
            self.addFact(fact, score)

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
