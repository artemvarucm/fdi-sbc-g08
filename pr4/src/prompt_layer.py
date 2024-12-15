class PromptLayer:
    """
    Capa padre para que los layers tengan el mismo método y se puedan ejecutar com pipeline
    """
    def chat(self, ollama, messagesHistory, query):
        pass
