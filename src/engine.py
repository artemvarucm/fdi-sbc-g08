from hornyClause import HornClause
from facts import Facts
from baseReglas import BaseReglas


class Engine:
    def __init__(self, base, modoDifusa):
        self.baseReglas = BaseReglas()
        self.facts = Facts()
        self.modoDifusa = modoDifusa

        for r in base:
            try:
                if ":-" in r:
                    self.baseReglas.addFromString(r)
                else:
                    self.newFact(r)
            except Exception:
                raise Exception(
                    f'Error al procesar la línea de la base de conocimiento: "{r}"'
                )

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

    def backward_chain(self, goals, showAppliedChain=True):
        """
        Aplica el razonamiento hacia atrás, incorporando lógica difusa

        showAppliedChain indica si hay que mostrar derivación

        Devuelve el grado de verdad de que ocurran todos los goals (AND)
        """
        score = 1
        for g in goals:
            if not self.facts.contains(g):
                for r in self.baseReglas.findByConsecuente(g):
                    # Recorremos las reglas cuyo consecuente sea la meta
                    if showAppliedChain:
                        r.print()

                    scorePrecedentes = self.backward_chain(
                        r.getAntecedentes(), showAppliedChain
                    )
                    scoreClausula = self.andDifuso(r.getGradoVerdad(), scorePrecedentes)

                    # Asignamos el nuevo grado de verdad de la meta
                    self.facts.addOrUpdateFact(
                        g,
                        self.orDifuso(
                            scoreClausula,
                            self.facts.getValorVerdad(g),
                        ),
                    )
                    if showAppliedChain and (scorePrecedentes > 0):
                        print(f"{g} [{self.facts.getValorVerdad(g)}]")

            elif showAppliedChain:
                print(f"{g} [{self.facts.getValorVerdad(g)}]")

            # Aplicamos AND entre los grados de verdad de las metas
            score = self.andDifuso(score, self.facts.getValorVerdad(g))

            # Podamos, no tiene sentido seguir, el grado será 0 como máximo
            if score == 0:
                break

        return score
