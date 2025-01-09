class InvalidFileExtensionError(Exception):
    """Excepción personalizada para extensiones de archivo no válidas."""
    def __init__(self, message="[ERROR]: El archivo debe tener extension PNG"):
        self.message = message
        super().__init__(self.message)