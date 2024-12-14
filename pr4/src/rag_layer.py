from utils import readFile
from pathlib import Path
from autocorrect import Speller
from prompt_layer import PromptLayer

class RAGLayer(PromptLayer):
    """
    Clase encargada de hacer el prompt engineering con ollama (intermediario)
    """

    def __init__(self, bases_conocimiento, mappings):
        self.mappings = mappings
        self.bases_conocimiento = bases_conocimiento

    """def processKnowledge(self, query):
        contextLines = []
        for k in self.knowledge.keys():
            if k in query.lower():
                contextLines.extend(readFile(self.knowledge[k]))

        print(" ".join(contextLines))
        return " ".join(contextLines)
    """

    def correct_query(self, query):
        """Recibe una consulta y la corrige en caso de que el usuario la haya escrito mal"""
        spell = Speller(lang="en")
        query = spell(query)

        return query

    def chat(self, ollama, messagesHistory, query):
        query_correct = self.correct_query(query)
        print(readFile(self.mappings))
        messagesHistory.extend(
            [
                {
                    "role": "system",
                    "content": f"""
                        Find the most relevant paths given this description
                        {" ".join(readFile(self.mappings))}
                        
                        To answer this question
                        {query_correct}

                        Return it as a list of paths, excluding any extra information, so I can save it as a python list.
                    """,
                }
            ]
        )

        selectedPaths = ollama.chat(messagesHistory)
        print(selectedPaths)

        # Añadimos la respuesta de ollama al historial
        messagesHistory.append(selectedPaths["message"])