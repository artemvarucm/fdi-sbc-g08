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

    def __init__(self, bases_conocimiento, mappings_path):
        self.bases_conocimiento = bases_conocimiento
        with open(mappings_path, "r") as file:
            try:
                self.mappings = json.load(file)
            except Exception as e:
                raise Exception(f"[FATAL ERROR] When reading the mappings from {mappings_path}. {e}")

    def correct_query(self, query):
        """Recibe una consulta y la corrige en caso de que el usuario la haya escrito mal"""
        spell = Speller(lang="en")
        query = spell(query)

        return query
    
    def match_mappings_ollama(self, ollama, query):
        ollamaMappings = self.mappings["ollama"]
        messagesRAG = [
            {
                "role": "system",
                "content": f"""
                    Given the following information about paths:
                    {str(ollamaMappings)}

                    Identify the path which is the most relevant for this query "{query}".
                    Return only the path, without any explanation.
                """,
            }
        ]

        response = ollama.chat(messagesRAG)
        responseContent = response["message"]["content"]
        dirs = set()
        for k in ollamaMappings.keys():
            if k in responseContent:
                dirs.add(Path(self.bases_conocimiento, k))

        return dirs

    def match_mappings_keywords(self, query):
        keywordsMappings = self.mappings["keywords"]
        dirs = set()
        for k in keywordsMappings.keys():
            if k in query.lower():
                dirs.update([Path(self.bases_conocimiento, p) for p in keywordsMappings[k]])
        return dirs

    def chat(self, ollama, messagesHistory, query):
        query_correct = self.correct_query(query)
        matchedDirs = self.match_mappings_ollama(ollama, query_correct)
        matchedDirs = matchedDirs.union(self.match_mappings_keywords(query_correct))

        contextLines = []
        for dirPath in matchedDirs:
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
