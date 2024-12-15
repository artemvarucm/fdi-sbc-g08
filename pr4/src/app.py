import sys
from ollama_chat import OllamaChat


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(
        self, knowledge_path, mappings, model, chain_of_thought, debug
    ):
        self.ollama_chat = OllamaChat(
            knowledge_path, mappings, model, chain_of_thought, debug
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

    def changeAllParameters(self):
        """Cambia l"""
        try:
            self.ollama_chat.changeAllParameters()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")

    def changeAllParameters(self):
        """Cambia l"""
        try:
            self.ollama_chat.changeParameters()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
    
    def changeTemperature(self):
        try:
            self.ollama_chat.changeTemperature()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
    
    def change_maxTokens(self):
        try:
            self.ollama_chat.change_maxTokens()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
    
    def change_frequencyPenalty(self):
        try:
            self.ollama_chat.change_frequencyPenalty()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
    
    def change_n(self):
        try:
            self.ollama_chat.change_n()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
    
    def chat(self, query):
        """
        Transmite el mensaje a ollama e imprime la respuesta
        """
        response = self.ollama_chat.chat(query)
        print(response)

    def printStatus(self):
        """Muestra la configuracion actual"""
        self.ollama_chat.printStatus()

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
                elif "\\parameters" == query:
                    self.changeAllParameters()
                elif "\\temperature" == query:
                    self.changeTemperature()
                elif "\\tokens" == query:
                    self.change_maxTokens()
                elif "\\repetition" == query:
                    self.change_frequencyPenalty()
                elif "\\answers" == query:
                    self.change_n()
                elif "\\status" == query:
                    self.printStatus()
                else:
                    print("[ERROR]: COMMAND NOT FOUND, CHECK SYNTAX.")
            else:
                self.chat(query)

    def help(self):
        print(f"{'\\status':6} - Shows current program settings")
        print(f"{'\\model':6} - Change Ollama model")
        print(
            f"{'\\temperature':6} - Change Ollama temperature [0, 1]. Smaller values make responses more deterministic, bigger values result in more creative responses"
        )
        print(
            f"{'\\tokens':6} - Change Ollama maximum number of tokens for the response"
        )
        print(
            f"{'\\repetition':6} - Change Ollama frequency_penalisation [-2, 2]. Smaller values penalise less, bigger values penalise more"
        )
        print(
            f"{'\\answers':6} - Change Ollama number of answers"
        )
        print(f"{'\\help':6} - Shows help")
        print(f"{'\\quit':6} - Quit the program")
        print()
