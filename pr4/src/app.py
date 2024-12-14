import sys
from ollama_chat import OllamaChat
from utils import addFile
from pathlib import Path


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path, mappings, model, chain_of_thought):
        self.ollama_chat = OllamaChat(knowledge_path, mappings, model, chain_of_thought)
        self.knowledge_path = knowledge_path

    def model(self):
        """
        Cambia de modelo
        """
        model = input("Introduce el nombre del nuevo modelo: ")
        model = model.strip()
        self.ollama_chat.switchModel(model)

    def chat(self, query):
        """
        Transmite el mensaje a ollama e imprime la respuesta
        """
        response = self.ollama_chat.chat(query)
        print(response)

    def processCommand(self, query):
        """
        Ejecuta las acciones correspondientes al query indicado
        """
        query = query.strip()
        if query[0] == "\\":  # los comandos empiezan con \
            if "\\help" == query:
                self.help()
            elif "\\quit" == query:
                sys.exit(1)
            elif "\\model" == query:
                self.model()
            elif "\\add" in query:
                _, file_name, file_path_arg = query.split(" ")
                file_path = Path(self.knowledge_path, file_name)
                addFile(file_path, file_path_arg)
            else:
                print("[ERROR]: COMMAND NOT FOUND, CHECK SYNTAX.")
        else:
            self.chat(query)

    def help(self):
        print(f"{"\\model":6} - Change Ollama model")
        print(f"{"\\help":6} - Shows help")
        print(f"{"\\quit":6} - Quit the program")
        print()
