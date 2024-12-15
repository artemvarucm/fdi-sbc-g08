from rag_layer import RAGLayer
from chain_thought_layer import ChainThoughtLayer
from ollama_controller import OllamaController


class OllamaChat:
    """Clase encargada de realizar el prompt engineering al interactuar con Ollama"""

    def __init__(self, bases_conocimiento, mappings, model, chain_of_thought, debug):
        self.chain_of_thought = chain_of_thought
        self.messagesHistory = self.getInitPrompts()
        self.layers = [RAGLayer(bases_conocimiento, mappings, debug)]
        if self.chain_of_thought:
            self.layers.append(ChainThoughtLayer())

        self.ollama = OllamaController(model)

    def printStatus(self):
        """Muestra la configuracion actual"""
        print()
        self.ollama.printStatus()
        print(f"CHAIN OF THOUGHT: {self.chain_of_thought}")
        print()

    def switchModel(self, model):
        """Cambia de modelo ollama"""
        return self.ollama.setModel(model)

    def changeAllParameters(self):
        """Cambia todos los parámetros de ollama"""
        return self.ollama.changeAllParameters()

    def changeTemperature(self):
        """Cambia la temperatura de ollama"""
        self.ollama.changeTemperature()

    def changeMaxTokens(self):
        """Cambia el maximo de tokens de ollama"""
        self.ollama.changeMaxTokens()

    def changeFrequencyPenalty(self):
        """Cambia la penalización de frecuencia de ollama"""
        self.ollama.changeFrequencyPenalty()

    def changeN(self):
        """Cambia el numerod e respuestas de ollama"""
        self.ollama.changeN()

    def chat(self, query):
        """Manda el nuevo mensaje a ollama, pasando por el pipeline de capas"""
        for l in self.layers:
            l.chat(self.ollama, self.messagesHistory, query)

        return self.messagesHistory[-1]["content"]  # devuelve el último mensaje

    def getInitPrompts(self):
        """Prompts iniciales para indicar a ollama de qué se encargará"""
        prompts = [
            {
                "role": "system",
                "content": """
                You are a salesman that helps people to find out which car is available and
                why is it better from the knowledge base we will provide you. 
                You must be efficient, using only the right information to answer the response from the user.
            """,
            },
            {
                "role": "system",
                "content": """
                 If you do not find the information in the knowledge we provide you, 
                 answer whatever you consider relevant. 
            """,
            },
        ]

        return prompts
