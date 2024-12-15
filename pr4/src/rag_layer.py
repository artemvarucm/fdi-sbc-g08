from utils import readFile
from pathlib import Path
from autocorrect import Speller
from prompt_layer import PromptLayer
import json
import os


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
        messagesRAG = [
            {
                "role": "system",
                "content": f"""
                    Given the following information about paths:
                    {" ".join(readFile(self.mappings))}

                    Identify the path which is the most relevant for this query "{query_correct}".
                    Return only the path, without any explanation.
                """,
            }
        ]

        selectedPathsRaw = ollama.chat(messagesRAG)

        # messagesRAG.append(selectedPathsRaw["message"])
        contextLines = []
        with open(self.mappings, "r") as file:
            data = json.load(file)
            for k in data.keys():
                if k in selectedPathsRaw["message"]["content"]:
                    dirPath = Path(self.bases_conocimiento, k)
                    for filename in os.listdir(dirPath):
                        file_path = Path(dirPath, filename)
                        if os.path.isfile(file_path):
                            contextLines.extend(readFile(file_path))

        messagesHistory.extend(
            [
                {
                    "role": "system",
                    "content": (
                        f"For the next user query use the following context {' '.join(contextLines)}."
                        if contextLines
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
