class HornClause:
    def __init__(self, clausula):
        self.obtenerClausula(clausula)

    def obtenerClausula(self, clausula):
        descomposicion = clausula.split(" :- ")
        self.consecuente = descomposicion[0]
        descomposicion = descomposicion[1].replace(",", "")

        descomposicion = descomposicion.split(" ")
        self.prob = float(descomposicion[-1][1:-1])

        self.antecedentes = set(descomposicion[:-1])

        print(self.consecuente, self.antecedentes, self.prob)
    