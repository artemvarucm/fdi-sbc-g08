from rag_layer import RAGLayer
from chain_thought_layer import ChainThoughtLayer
from ollama_controller import OllamaController

class OllamaChat:
    def __init__(self, bases_conocimiento, mappings, model, chain_of_thought):
        self.messagesHistory = self.getInitPrompts()
        self.layers = [RAGLayer(bases_conocimiento, mappings)]
        if chain_of_thought:
            self.layers.append(ChainThoughtLayer())

        self.ollama = OllamaController(model)

    def switchModel(self, model):
        return self.ollama.setModel(model)

    def chat(self, query):
        for l in self.layers:
            l.chat(self.ollama, self.messagesHistory, query)

        return self.messagesHistory[-1]["content"] # devuelve el último mensaje
    
    def getInitPrompts(self):
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