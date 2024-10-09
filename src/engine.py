from hornyClause import HornClause
from facts import Facts
from baseReglas import BaseReglas


class Engine:
    def __init__(self, baseReglas):
        self.baseReglas = BaseReglas()
        self.facts = Facts()
        for r in baseReglas:
            if ":-" in r:
                self.baseReglas.add(r)
            else:
                self.newFact(r)

    def print(self):
        """
        Muestra las clausulas y hechos de la base de conocimiento
        """
        print("HORNY CLAUSES")
        self.baseReglas.print()
        print("-" * 10)
        print("FACTS")
        self.facts.print()
        print()

    def newFact(self, factStr):
        """
        Añade un nuevo hecho a partir de la cadena factStr

        Si existe, lanza una excepción
        """
        factArray = factStr.split(" ")
        fact = factArray[0]
        prob = 1

        # si no se ha indicado el grado de verdad asumimos que es 1

        if len(factArray) > 1:
            prob = float(factArray[1][1:-1])

        self.facts.addFact(fact, prob)

    def evaluar(self, prob):
        if prob == 1:
            print("Si")
        elif prob >= 0.7:
            print(f"Si, mucho ({prob})")
        else:
            print("No")

    # fixme
    # def evaluar
    # min/max
    # libreria click
    def backward_chain(self, goals):
        prob = 1
        for g in goals:
            if not self.facts.contains(g):
                for r in self.baseReglas.findByConsecuente(g):
                    r.print()

                    probPrecedentes = self.backward_chain(r.getAntecedentes())

                    self.facts.addOrUpdateFact(
                        g,
                        max(
                            r.getGradoVerdad() * probPrecedentes,
                            self.facts.getValorVerdad(g),
                        ),
                    )

            prob *= self.facts.getValorVerdad(g)

        return prob
