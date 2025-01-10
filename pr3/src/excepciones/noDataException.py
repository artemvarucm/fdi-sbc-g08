from .customException import CustomException


class NoDataException(CustomException):
    """Excepción personalizada para cuando no haya datos que dibujar"""

    def __init__(self, message="[ERROR]: No hay datos para dibujar el grafo"):
        self.message = message
        super().__init__(self.message)
