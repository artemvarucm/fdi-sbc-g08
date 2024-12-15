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
            "temperature": 0.5,
            "max_tokens": 400,
            "frequency_penalty": 0.0,
            "stream": True,
            "n": 1,
        }
        self.setModel(model)

    def changeParameters(self, temperature):
        """Configura los parámetros de ollama"""
        try:
            self.options["temperature"] = float(input("Enter temperature: "))
            self.options["max_tokens"] = float(input("Enter the max tokens: "))
            self.options["frequency_penalty"] = float(
                input("Enter the frequency penalty: ")
            )
            self.options["n"] = float(input("Enter the number of answers: "))
        except KeyboardInterrupt:
            print("\n[INFO] OPERATION INTERRUPTED BY USER.")
        except ValueError:
            print("\n[ERROR] NUMBER MUST BE FLOAT.")

    def printStatus(self):
        """Muestra la configuracion actual"""
        print(f"OLLAMA MODEL: {self.model}")
        print(f"OLLAMA TEMPERATURE: {self.temperature}")

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
