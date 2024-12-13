from utils import readFile
from ollama_controller import OllamaController
import os
from pathlib import Path

class RAG:
    """
    Clase encargada de hacer el prompt engineering con ollama (intermediario)
    """

    def __init__(self, bases_conocimiento, model):
        self.knowledge = self.loadKnowledge(bases_conocimiento)
        self.messagesHistory = self.getPrompts()
        self.ollama = OllamaController(model)
    
    def loadKnowledge(self, bases_conocimiento):
        return {
            "ferrari": Path(bases_conocimiento,"ferrari.txt"),
            "bugatti": Path(bases_conocimiento,"bugatti.txt")
        }

    def processKnowledge(self, query):
        contextLines = []
        for k in self.knowledge.keys():
            if k in query.lower():
                contextLines.extend(readFile(self.knowledge[k]))

        print(" ".join(contextLines))
        return " ".join(contextLines)
    
    def chat(self, query):
        processed = self.processKnowledge(query)
        self.messagesHistory.extend([
            {
                "role": "system",
                "content": f"For the next user query use the following context {processed}." if processed else "Try to find information from your own knowledge."
            },
            {
                "role": "user",
                "content": query,
            }
        ])
        response = self.ollama.chat(self.messagesHistory)

        # Añadimos la respuesta de ollama al historial
        self.messagesHistory.append(response["message"])

        return response["message"]["content"]

    def switchModel(self, model):
        return self.ollama.setModel(model)

    def getPrompts(self):
        return [
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
            }
        ]
