import sys
from rag import RAG

class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path):
        self.rag = RAG(knowledge_path)

    def model(self):
        """
        Cambia de modelo
        """
        model = input("Introduce el nombre del nuevo modelo: ")
        model = model.strip()
        self.rag.switchModel(model)

    def chat(self, query):
        """
        Transmite el mensaje a ollama e imprime la respuesta
        """
        response = self.rag.chat(query)
        print(response)

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        query = query.strip()
        if "\\help" == query:
            self.help()
        elif "\\quit" == query:
            sys.exit(1)
        else:
            self.chat(query)

    def help(self):
        print(f"{"\\model":28} - cambiar de modelo ollama")
        print(f"{"\\help":28} - muestra los comandos del programa")
        print(f"{"\\quit":28} - salir del programa")
        print()
