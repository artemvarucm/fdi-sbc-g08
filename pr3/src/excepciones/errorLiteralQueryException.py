from .customException import CustomException

class ErrorLiteralQueryException(CustomException):
    """Excepción personalizada para cuando el usuario no cierre las comillas del literal en el where de una consulta"""

    def __init__(self, message="[ERROR]: En el where de la query le ha faltado cerrar las comillas de algún literal"):
        self.message = message
        super().__init__(self.message)
