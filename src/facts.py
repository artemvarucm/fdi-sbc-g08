class Facts:
    '''
    Estructura de datos para almacenar los 
    hechos con sus respectivos grados de verdad
    '''
    def __init__(self):
        self.container = {}
    
    def addOrUpdateFact(self, fact, prob):
        '''
        Actualiza o añade información sobre el hecho
        '''
        self.container[fact] = prob
    
    def contains(self, fact):
        '''
        Devuelve true si un hecho tiene grado de verdad mayor que 0
        '''
        return (fact in self.container) and (self.container[fact] > 0)
    
    def getValorVerdad(self, fact):
        '''
        Devuelve el grado de verdad de un hecho
        '''
        if fact in self.container:
            return self.container[fact]
        
        return 0