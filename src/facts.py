class Facts:
    '''
    Estructura de datos para almacenar los 
    hechos con sus respectivas probabilidades
    '''
    __init__(self):
        self.container = {}
    
    def addOrUpdateFact(self, fact, prob):
        '''
        Actualiza o añade información sobre el hecho
        '''
        self.container[fact] = prob
    


