class CustomException(Exception):
    """Clase para detectar excepciones cuyo motivo se conoce"""

    def __init__(self, message):
        super().__init__(message)
