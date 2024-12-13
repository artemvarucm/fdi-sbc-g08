import sys
from rag import RAG


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path, model):
        self.rag = RAG(knowledge_path, model)

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
        if query[0] == "\\": # los comandos empiezan con \
            if "\\help" == query:
                self.help()
            elif "\\quit" == query:
                sys.exit(1)
            elif "\\model" == query:
                self.model()
            else:
                print("[ERROR]: COMMAND NOT FOUND, CHECK SYNTAX.")
        else:
            self.chat(query)

    def help(self):
        print(f"{"\\model":6} - Change Ollama model")
        print(f"{"\\help":6} - Shows help")
        print(f"{"\\quit":6} - Quit the program")
        print()
