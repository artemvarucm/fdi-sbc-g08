import ollama
from ollama import chat
from ollama import ChatResponse


class OllamaController:
    """
    Clase que se encarga de realizar las consultas a las API de ollama
    """

    def __init__(self, model):
        self.model = None
        self.options = {
            "temperature": 0.7,
            "max_tokens": 4000,
            "frequency_penalty": 0.0,
            "n": 1,
        }
        self.setModel(model)

    def changeTemperature(self):
        """Cambia la temperatura de ollama"""
        while True:
            try:
                self.options["temperature"] = float(input("Enter temperature: "))
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE FLOAT BETWEEN 0 AND 1")

    def changeMaxTokens(self):
        """Cambia el maximo de tokens de ollama"""
        while True:
            try:
                self.options["max_tokens"] = int(input("Enter the max tokens: "))
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE INTEGER")

    def changeFrequencyPenalty(self):
        """Cambia la penalización de frecuencia de ollama"""
        while True:
            try:
                self.options["frequency_penalty"] = float(
                    input("Enter the frequency penalty: ")
                )
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE FLOAT BETWEEN -2 AND 2")

    def changeN(self):
        """Cambia el numerod e respuestas de ollama"""
        while True:
            try:
                self.options["n"] = int(input("Enter the number of answers: "))
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE INTEGER")

    def changeAllParameters(self, temperature):
        """Cambia todos los parámetros de ollama"""
        self.changeTemperature()
        self.change_maxTokens()
        self.change_frequencyPenalty()
        self.change_n()

    def printStatus(self):
        """Muestra la configuracion actual"""
        print(f"OLLAMA MODEL: {self.model}")
        print(f"----OLLAMA PARAMETERS----")
        print(f"    TEMPERATURE: {self.options['temperature']}")
        print(f"    MAX_TOKENS: {self.options['max_tokens']}")
        print(f"    FREQUENCY_PENALTY: {self.options['frequency_penalty']}")
        print(f"    N: {self.options['n']}")

    def setModel(self, model):
        """
        Cambia de modelo de ollama
        """
        try:
            # probamos enviar consulta para ver si el modelo está instalado
            ollama.chat(model=model, messages=[{"role": "user", "content": "Hello!"}])

            self.model = model
            print(f'[INFO]: MODEL "{model}" LOADED. TO SWAP EXECUTE \\model')
        except ollama.ResponseError as e:
            if e.status_code == 404:
                # Descarga el modelo si no lo encuentra
                print(f'[INFO]: DOWNLOADING "{model}" MODEL.')
                try:
                    ollama.pull(model)
                    self.model = model
                    print(f'[INFO]: MODEL "{model}" LOADED. TO SWAP EXECUTE \\model')
                except Exception as e:
                    print(f'[OLLAMA ERROR]: ERROR WHEN DOWNLOADING "{model}" MODEL.')
            else:
                print("[OLLAMA ERROR]:", e.error)
        except Exception as e:
            raise Exception(
                "[FATAL ERROR] CAN'T CONNECT TO OLLAMA SERVER. CHECK IF SERVER IS RUNNING."
            )

    def chat(self, messagesHistory):
        """Manda el historial del chat (con el nuevo mensaje), al modelo y devuelve su respuesta"""
        if self.model is None:
            raise Exception("YOU NEED TO SPECIFY A VALID OLLAMA MODEL, EXECUTE \\model")
        else:
            response: ChatResponse = chat(
                model=self.model,
                messages=messagesHistory,
                options=self.options,
            )
            return response
