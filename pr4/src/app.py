import sys
from ollama_chat import OllamaChat


class App:
    """
    Aplicación principal que se encarga de
    ejecutar las acciones de los comandos
    """

    def __init__(self, knowledge_path, mappings, model, chain_of_thought, debug):
        self.ollama_chat = OllamaChat(
            knowledge_path, mappings, model, chain_of_thought, debug
        )

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
        """Cambia todos los parametros de ollama"""
        try:
            self.ollama_chat.changeAllParameters()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")

    def changeTemperature(self):
        try:
            self.ollama_chat.changeTemperature()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")

    def changeMaxTokens(self):
        try:
            self.ollama_chat.changeMaxTokens()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")

    def changeFrequencyPenalty(self):
        try:
            self.ollama_chat.changeFrequencyPenalty()
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")

    def changeN(self):
        try:
            self.ollama_chat.changeN()
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

    def toggleOllamaMap(self):
        self.ollama_chat.toggleOllamaMap()

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
                    self.changeMaxTokens()
                elif "\\repetition" == query:
                    self.changeFrequencyPenalty()
                elif "\\answers" == query:
                    self.changeN()
                elif "\\status" == query:
                    self.printStatus()
                elif "\\tgl_ollama_map" == query:
                    self.toggleOllamaMap()
                else:
                    print("[ERROR]: COMMAND NOT FOUND, CHECK SYNTAX.")
            else:
                self.chat(query)

    def help(self):
        print(f"{'\\status':15} - Shows current program settings")
        print(f"{'\\model':15} - Change Ollama model")
        print(f"{'\\parameters':15} - Change all Ollama parameters")
        print(
            f"{'\\temperature':15} - Change Ollama temperature [0, 1]. Smaller values make responses more deterministic, bigger values result in more creative responses"
        )
        print(
            f"{'\\tokens':15} - Change Ollama maximum number of tokens for the response"
        )
        print(
            f"{'\\repetition':15} - Change Ollama frequency_penalisation [-2, 2]. Smaller values penalise less, bigger values penalise more"
        )
        print(f"{'\\answers':15} - Change Ollama number of answers")
        print(
            f"{'\\tgl_ollama_map':15} - Enables/Disables the Ollama mapping for the RAG. (only use keywords mapping or additional Ollama mapping too)."
        )
        print(f"{'\\help':15} - Shows help")
        print(f"{'\\quit':15} - Quit the program")
        print()
