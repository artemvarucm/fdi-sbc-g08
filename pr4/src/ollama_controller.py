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
                temp = float(input("Enter temperature: "))
                if temp < 0 or temp > 1:
                    raise ValueError()
                self.options["temperature"] = temp
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE FLOAT BETWEEN 0 AND 1")

    def changeMaxTokens(self):
        """Cambia el maximo de tokens de ollama"""
        while True:
            try:
                tokens = float(input("Enter the max tokens: "))
                if tokens < 0:
                    raise ValueError()
                self.options["max_tokens"] = tokens
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE INTEGER AND >0")

    def changeFrequencyPenalty(self):
        """Cambia la penalización de frecuencia de ollama"""
        while True:
            try:
                f = float(input("Enter the frequency penalty: "))
                if f < -2 or f > 2:
                    raise ValueError()
                self.options["frequency_penalty"] = f
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE FLOAT BETWEEN -2 AND 2")

    def changeN(self):
        """Cambia el numerod e respuestas de ollama"""
        while True:
            try:
                n = float(input("Enter the number of answers: "))
                if n < 0:
                    raise ValueError()
                self.options["n"] = n
                break
            except ValueError:
                print("\n[ERROR] NUMBER MUST BE INTEGER AND >0")

    def changeAllParameters(self):
        """Cambia todos los parámetros de ollama"""
        self.changeTemperature()
        self.changeMaxTokens()
        self.changeFrequencyPenalty()
        self.changeN()

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
