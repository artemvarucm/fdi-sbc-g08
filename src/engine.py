from hornyclause import HornClause

class Engine:
    def __init__(self, baseReglas):
        # base reglas es una lista de lineas del archivo, lo convertimos a objetos
        self.baseReglas = [HornClause(r) for r in baseReglas]

    def print(self):
        for r in self.baseReglas:
            r.print()


    def rules_match(rule1, rule2):
        return True

    def backward_chain(goals): #eliminar la regla que acabamos de aplicar
        for g in goals:
            if g in facts:
                continue
            else:
                for r in reglas:
                    if consecuente(r) == g and backward_chain(precedentes(r)):
                        facts.append(g)
                        break
                if g in facts:
                    continue
                else:
                    return False
                        
                
