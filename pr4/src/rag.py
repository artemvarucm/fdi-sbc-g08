from utils import readFile
from ollama_controller import OllamaController

class RAG:
    """
    Clase encargada de hacer el prompt engineering con ollama (intermediario)
    """
    def __init__(self, knowledge_path):
        print(f'[INFO]: CARGANDO BASE DE CONOCIMIENTO.')
        self.knowledge = " ".join(readFile(knowledge_path))
        print(f'[INFO]: CARGA REALIZADA CORRECTAMENTE.')
        self.ollama = OllamaController()
        self.ollama.setMessageHistory(self.getPrompts())

    def chat(self, query):
        return self.ollama.chat(query)

    def switchModel(self, model):
        return self.ollama.setModel(model)
    
    def getPrompts(self):
        return [
        {
            "role": "system",
            "content": "Remember this: " + self.knowledge,
        },
        {
            "role": "system",
            "content": """
                You are an expert assistant in semantic networks and knowledge bases. 
                Your task is to answer questions related to RDF, SPARQL, and related concepts, 
                using the provided base as a reference.
            """,
        }]
        