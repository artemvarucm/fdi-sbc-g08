from .customException import CustomException

class InvalidFileExtensionException(CustomException):
    """Excepción personalizada para extensiones de archivo no válidas."""
    def __init__(self, message="[ERROR]: El archivo debe tener extension PNG"):
        self.message = message
        super().__init__(self.message)