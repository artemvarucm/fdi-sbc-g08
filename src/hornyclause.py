import re

class HornClause:
    def __init__(self, clausula):
        self.obtenerClausula(clausula)

    def print(self):
        '''
        Muestra la clausula de Horn segun el formato definido
        '''
        print(f"{self.consecuente} :- {', '.join(self.antecedentes)} [{self.prob}]")
    
    def getConsecuente(self):
        return self.consecuente
    
    def getAntecedentes(self):
        return self.antecedentes

    def getGradoVerdad(self):
        return self.prob

    def obtenerClausula(self, clausula):
        '''
        Descompone la clausula de horn en formato texto para inicializarla como objeto
        '''

        descomposicion = clausula.split(" :- ")
        # El consecuente es el primer elemento del array separado
        self.consecuente = descomposicion[0]

        # El grado de verdad está entre corchetes, lo sacamos con regex
        self.prob = 1. # por defecto es 1

        probStr = re.findall(r"\[(.*)\]", descomposicion[1])
        if (probStr):
            self.prob = float(probStr[0])

        # Para el regex de los precedentes nos fijamos en los caracteres del abecedario y el guion bajo
        self.antecedentes = set(re.findall(r"([A-Za-z_]+),?", descomposicion[1]))
    