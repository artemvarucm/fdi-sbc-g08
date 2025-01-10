from .customException import CustomException


class FileNotFoundException(CustomException):
    """Excepción personalizada para cuando no existe el archivo accedido"""

    def __init__(self, file_path):
        super().__init__(f'[ERROR]: Archivo "{file_path}" no encontrado.')
