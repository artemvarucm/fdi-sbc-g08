from .customException import CustomException


class FileAlreadyExistsException(CustomException):
    """Excepción personalizada para cuando el archivo donde se quiere guardar ya existe"""

    def __init__(self, message):
        super().__init__(message)
