import sys
from ollama_chat import OllamaChat

class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path, mappings, model, temperature, chain_of_thought, debug):
        self.ollama_chat = OllamaChat(
            knowledge_path, mappings, model, temperature, chain_of_thought, debug
        )
        self.knowledge_path = knowledge_path

    def model(self):
        """
        Cambia de modelo
        """
        try:
            model = input("Enter model name: ")
            model = model.strip()
            if model:
                self.ollama_chat.switchModel(model)
            else:
                print("\n[ERROR] MODEL NAME CAN'T BE BLANK.")
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")

    def setTemperature(self):
        """Cambia la temperatura"""
        try:
            temp = float(input("Enter temperature: "))
            self.ollama_chat.setTemperature(temp)
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
        except ValueError:
            print("\n[ERROR] TEMPERATURE MUST BE FLOAT.")

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
        if query:
            if query[0] == "\\":  # los comandos empiezan con \
                if "\\help" == query:
                    self.help()
                elif "\\quit" == query:
                    sys.exit(1)
                elif "\\model" == query:
                    self.model()
                elif "\\temp" == query:
                    self.setTemperature()
                else:
                    print("[ERROR]: COMMAND NOT FOUND, CHECK SYNTAX.")
            else:
                self.chat(query)

    def help(self):
        print(f"{'\\model':6} - Change Ollama model")
        print(f"{'\\temp':6} - Change Ollama temperature. Smaller values (< 0.5) make responses more deterministic, bigger values (> 1.0) result in more creative responses")
        print(f"{'\\help':6} - Shows help")
        print(f"{'\\quit':6} - Quit the program")
        print()
