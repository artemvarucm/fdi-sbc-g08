import ollama
from ollama import chat
from ollama import ChatResponse


class OllamaController:
    """
    Clase que se encarga de realizar las consultas a las API de ollama
    """

    def __init__(self, model="llama3.2:3b"):
        self.setModel(model)
        self.messagesHistory = []
        print(f'[INFO]: MODELO CARGADO "{model}". Para cambiar ejecute \\model')

    def setMessageHistory(self, messagesHistory):
        """
        Reinicia la secuencia del chat al contenido del parámetro (se usa para el prompt engineering)
        """
        self.messagesHistory = messagesHistory

    def setModel(self, model):
        """
        Cambia de modelo de ollama
        """
        self.model = model
        # fixme error, model doesnt exist
        """except ollama.ResponseError as e:
            
            if e.status_code == 404:
                # Descarga el modelo si no lo encuentra
                print(f'[INFO]: DESCARGANDO MODELO "{model}".')
                try:
                    ollama.pull(model)
                    print(f'[INFO]: MODELO CARGADO "{model}". Para cambiar ejecute \\model')
                except Exception as e:
                    print(f'[OLLAMA ERROR]: ERROR AL INTENTAR DESCARGAR EL MODELO "{model}".')
            else:
                print('[OLLAMA ERROR]:', e.error)"""

    def chat(self, query):
        self.messagesHistory.append(
            {
                "role": "user",
                "content": query,
            }
        )

        response: ChatResponse = chat(model=self.model, messages=self.messagesHistory)

        # Añadimos la respuesta de ollama al historial
        self.messagesHistory.append(response["message"])

        return response["message"]["content"]
