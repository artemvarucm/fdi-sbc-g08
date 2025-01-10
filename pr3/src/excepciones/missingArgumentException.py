from .customException import CustomException


class MissingArgumentException(CustomException):
    """Excepción personalizada para cuando el comando se ejecuta sin argumentos"""

    def __init__(self, argname, message="[ERROR]: Este comando necesita el argumento"):
        self.message = message
        super().__init__(self.message + f" <{argname}>.")
