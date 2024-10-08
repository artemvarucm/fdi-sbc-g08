from hornyclause import HornClause
from facts import Facts

class Engine:
    def __init__(self, baseReglas):
        # base reglas es una lista de lineas del archivo, lo convertimos a objetos
        self.baseReglas = [HornClause(r) for r in baseReglas]
        self.facts = Facts()
    
    def print(self):
        '''
        Muestra las clausulas de la base de conocimiento
        '''
        for r in self.baseReglas:
            r.print()

    def newFact(self, factStr):
        '''
        Añade un nuevo hecho a partir de la cadena factStr

        Si existe, lanza una excepción
        '''
        factArray = factStr.split(" ")
        fact = factArray[0]
        prob = 1

        # si no se ha indicado el grado de verdad asumimos que es 1
        
        if len(factArray) > 1:
            prob = float(factArray[1] [1:-1])
        if (self.facts.contains(fact)):
            raise Exception(f"Hecho {fact} ya añadido.")

        self.facts.addOrUpdateFact(fact, prob)

    def evaluar(self, prob):
        if prob == 1:
            print("Si")
        elif prob >= 0.7:
            print(f"Si, mucho ({prob})")
        else:
            print("No")


# fixme
# def evaluar 
# eliminar la regla que acabamos de aplicar (baseReglas)
# min/max
# libreria click
    def backward_chain(self, goals): 
        prob = 1
        for g in goals:
            if not self.facts.contains(g):
                for r in self.baseReglas:
                    if r.getConsecuente() == g:
                        r.print()
                        probPrecedentes = self.backward_chain(r.getAntecedentes())
                        self.facts.addOrUpdateFact(
                            g, max(r.getGradoVerdad() * probPrecedentes, self.facts.getValorVerdad(g))
                        )

            prob *= self.facts.getValorVerdad(g)

        return prob
