from .customException import CustomException


class ErrorLiteralQueryException(CustomException):
    """Excepción personalizada para cuando el usuario no cierre las comillas del literal en el where de una consulta"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
