from facts import Facts
from baseReglas import BaseReglas
from knowledgeException import KnowledgeException


class Engine:
    def __init__(self, base, modoDifusa):
        self.baseReglas = BaseReglas()
        self.facts = Facts()
        self.modoDifusa = modoDifusa
        errores = False
        for r in base:
            try:
                if ":-" in r:
                    self.baseReglas.addFromString(r)
                else:
                    self.newFact(r)
            except KnowledgeException as e:
                errores = True
                print("[ERROR]:", e)

        errorStr = " excluyendo lineas con errores" if errores else " correctamente"
        print(f"\n[INFO] Base de conocimiento cargada{errorStr}.\n")

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
        if len(factArray) > 2:
            raise KnowledgeException(
                f"El formato de este hecho '{factStr}' tiene que ser: <hecho> [<grado de verdad>]"
            )

        fact = factArray[0]
        score = 1

        # si no se ha indicado el grado de verdad asumimos que es 1

        if len(factArray) == 2:
            if factArray[1][0] == "[" and factArray[1][-1] == "]":
                try:
                    score = float(factArray[1][1:-1])
                except ValueError:
                    raise KnowledgeException(
                        f"El grado de verdad del hecho '{factStr}' debe ser un numero."
                    )
            else:
                raise KnowledgeException(
                    f"El hecho '{factStr}' debe llevar el grado de verdad entre corchetes: <hecho> [<grado de verdad>]"
                )

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
