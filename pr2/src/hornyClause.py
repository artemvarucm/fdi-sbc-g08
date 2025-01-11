from knowledgeException import KnowledgeException


class HornClause:
    """
    Representa una clausula de Horn
    a :- b, c [0.5]
    (consecuente, precedentes y grado de verdad)
    """

    def __init__(self, clausula):
        self.obtenerClausula(clausula)

    def print(self):
        """
        Muestra la clausula de Horn segun el formato definido
        """
        print(f"{self.consecuente} :- {', '.join(self.antecedentes)} [{self.score}]")

    def obtenerClausula(self, clausulaStr):
        """
        Descompone la clausula de horn en formato texto para inicializarla como objeto
        """

        descomposicion = clausulaStr.split(" :- ")
        if len(descomposicion) != 2:
            raise KnowledgeException(
                f"El formato de la clausula '{clausulaStr}' tiene que ser: <consecuente> :- <precedentes> [<opcional, grado de verdad>]"
            )

        # Leemos el consecuente
        self.consecuente = descomposicion[0].strip()
        precedentes = descomposicion[1]

        # Leemos el grado de verdad (si está indicado)
        self.score = 1.0  # por defecto es 1
        if "[" in precedentes or "]" in precedentes:
            if "[" in precedentes and precedentes[-1] == "]":
                try:
                    corchete1 = precedentes.find("[") + 1
                    self.score = float(precedentes[corchete1:-1])

                    # eliminamos del string de precedentes el grado de certeza para que no interfiera
                    precedentes = precedentes[: corchete1 - 1]
                    if self.score > 1 or self.score < 0:
                        raise KnowledgeException(
                            "El grado de certeza tiene que estar entre 0 y 1."
                        )

                except ValueError:
                    raise KnowledgeException(
                        f"El grado de verdad de la clausula '{clausulaStr}' debe ser un numero."
                    )
            else:
                raise KnowledgeException(
                    f"La clausula '{clausulaStr}' debe llevar el grado de verdad al final y entre corchetes: <consecuente> :- <precedentes> [<opcional, grado de verdad>]"
                )

        # Leemos los antecedentes (separados por ,)
        parts = [part.strip() for part in precedentes.split(",")]
        if "" in parts:
            raise KnowledgeException(
                f"La clausula '{clausulaStr}' no puede llevar un precedente vacío (hay alguna coma que sobra)."
            )
        if any([" " in p for p in parts]):
            raise KnowledgeException(
                f"La clausula '{clausulaStr}' no puede llevar un precedente con espacios."
            )

        self.antecedentes = set(parts)

    def getConsecuente(self):
        return self.consecuente

    def getAntecedentes(self):
        return self.antecedentes

    def getGradoVerdad(self):
        return self.score
