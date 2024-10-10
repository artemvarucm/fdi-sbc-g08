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
        print("HORN CLAUSES")
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
        score = 1

        # si no se ha indicado el grado de verdad asumimos que es 1

        if len(factArray) > 1:
            score = float(factArray[1][1:-1])

        self.facts.addFact(fact, score)

    def andDifuso(self, score1, score2):
        """
        Operador AND con logica difusa

        Recibe 2 grados de verdad como parametros
        """
        if self.modoDifusa == "min/max":
            return min(score1, score2)
        else:
            return score1 * score2

    def orDifuso(self, score1, score2):
        """
        Operador OR con logica difusa

        Recibe 2 grados de verdad como parametros
        """
        if self.modoDifusa == "min/max":
            return max(score1, score2)
        else:
            return score1 + score2 - score1 * score2

    def backward_chain(self, goals):
        """
        Aplica el razonamiento hacia atrás, incorporando lógica difusa

        Devuelve el grado de verdad de que ocurran todos los goals (AND)
        """
        score = 1
        for g in goals:
            if not self.facts.contains(g):
                for r in self.baseReglas.findByConsecuente(g):
                    # Recorremos las reglas cuyo consecuente sea la meta
                    r.print()
                    scorePrecedentes = self.backward_chain(r.getAntecedentes())
                    scoreClausula = self.andDifuso(r.getGradoVerdad(), scorePrecedentes)

                    # Asignamos el nuevo grado de verdad de la meta
                    self.facts.addOrUpdateFact(
                        g,
                        self.orDifuso(
                            scoreClausula,
                            self.facts.getValorVerdad(g),
                        ),
                    )
            else:
                print(f"{g} [{self.facts.getValorVerdad(g)}]")

            # Aplicamos AND entre los grados de verdad de las metas
            score = self.andDifuso(score, self.facts.getValorVerdad(g))

        return score
