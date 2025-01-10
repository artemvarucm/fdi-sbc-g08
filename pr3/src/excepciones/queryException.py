from .customException import CustomException


class QueryException(CustomException):
    """Excepción personalizada para cuando hay un error de formato en la consulta (query)"""

    def __init__(self, message="[ERROR]: Consulta incorrecta."):
        self.message = message
        super().__init__(self.message)
