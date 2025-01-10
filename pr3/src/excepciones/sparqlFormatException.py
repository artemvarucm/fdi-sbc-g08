from .customException import CustomException


class SPARQLFormatException(CustomException):
    """Excepción personalizada para cuando hay un error de formato SPARQL"""

    def __init__(self, message="[ERROR]: SPARQL incorrecto."):
        self.message = message
        super().__init__(self.message)
