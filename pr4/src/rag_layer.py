from utils import readFile
from pathlib import Path
from autocorrect import Speller
from prompt_layer import PromptLayer

class RAGLayer(PromptLayer):
    """
    Clase encargada de hacer el prompt engineering con ollama (intermediario)
    """

    def __init__(self, bases_conocimiento, mappings):
        self.knowledge = self.loadKnowledge(bases_conocimiento)
        self.bases_conocimiento = bases_conocimiento
        #self.knowledge = mappings

    def loadKnowledge(self, bases_conocimiento):
            return {
                # Historia de las marcas
                # Pilotos Formula 1
                # Modelos de coches de las marcas
                "ferrari": Path(bases_conocimiento, "historia", "ferrari.txt"),
            }

    def processKnowledge(self, query):
        contextLines = []
        for k in self.knowledge.keys():
            if k in query.lower():
                contextLines.extend(readFile(self.knowledge[k]))

        print(" ".join(contextLines))
        return " ".join(contextLines)

    def correct_query(self, query):
        """Recibe una consulta y la corrige en caso de que el usuario la haya escrito mal"""
        spell = Speller(lang="en")
        query = spell(query)

        return query

    def chat(self, ollama, messagesHistory, query):
        query_correct = self.correct_query(query)
        processed = self.processKnowledge(query_correct)
        
        messagesHistory.extend(
            [
                {
                    "role": "system",
                    "content": (
                        f"For the next user query use the following context {processed}."
                        if processed
                        else "Try to find information from your own knowledge."
                    ),
                },
                {
                    "role": "user",
                    "content": query_correct,
                },
            ]
        )

        response = ollama.chat(messagesHistory)

        # Añadimos la respuesta de ollama al historial
        messagesHistory.append(response["message"])