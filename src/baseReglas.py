from hornyClause import HornClause


class BaseReglas:
    def __init__(self):
        self.container = {}

    def add(self, regla):
        clause = HornClause(regla)
        key = clause.getConsecuente()
        if key not in self.container:
            self.container[key] = []

        self.container[key].append(clause)

    def findByConsecuente(self, consecuente):
        if consecuente not in self.container:
            return []

        return self.container[consecuente]

    def print(self):
        for r in self.container:
            r.print()
