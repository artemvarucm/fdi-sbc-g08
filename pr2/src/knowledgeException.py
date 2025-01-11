class KnowledgeException(Exception):
    """Excepción personalizada para representar excepciones al leer la base de conocimiento"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
