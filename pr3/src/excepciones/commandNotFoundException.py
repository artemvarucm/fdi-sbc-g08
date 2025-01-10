from .customException import CustomException

class CommandNotFoundException(CustomException):
    """Excepción personalizada para cuando el comando introducido no se ha reconocido"""
    def __init__(self, message="[ERROR]: Comando desconocido. Revise la sintaxis."):
        self.message = message
        super().__init__(self.message)