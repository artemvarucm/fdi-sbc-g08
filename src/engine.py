from hornyClause import HornClause
from facts import Facts
from baseReglas import BaseReglas


class Engine:
    def __init__(self, base, modoDifusa):
        self.baseReglas = BaseReglas()
        self.facts = Facts()
        self.modoDifusa = modoDifusa
        for r in base:
            if ":-" in r:
                self.baseReglas.addFromString(r)
            else:
                self.newFact(r)

    def print(self):
        """
        Muestra las clausulas y hechos de la base de conocimiento
        """
        print("HORNY CLAUSES")
        self.baseReglas.print()
        print("-" * 15)

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
    
    def andDifuso(self, prob1, prob2):
        """
        Operador AND con logica difusa
        """
        if self.modoDifusa == "min/max":
            return min(prob1, prob2)
        else:
            return prob1 * prob2

    def orDifuso(self, prob1, prob2):
        """
        Operador OR con logica difusa
        """
        if self.modoDifusa == "min/max":
            return max(prob1, prob2)
        else:
            return prob1 + prob2 # ver la resta

    # fixme
    # def evaluar
    def backward_chain(self, goals):
        """
        Aplica el razonamiento hacia atrás, incorporando lógica difusa
        
        Devuelve el grado de verdad de que ocurran todos los goals
        """
        prob = 1
        for g in goals:
            if not self.facts.contains(g):
                for r in self.baseReglas.findByConsecuente(g):
                    r.print()

                    probPrecedentes = self.backward_chain(r.getAntecedentes())

                    self.facts.addOrUpdateFact(
                        g,
                        self.orDifuso(
                            self.andDifuso(r.getGradoVerdad(), probPrecedentes), # fixme AND vs MULTIPLICAR?
                            self.facts.getValorVerdad(g),
                        ),
                    )
            else:
                print(f"{g} [{self.facts.getValorVerdad(g)}]")

            prob = self.andDifuso(prob, self.facts.getValorVerdad(g))

        return prob
