import sys
import click
from utils import readFile
import ollama
from ollama import chat
from ollama import ChatResponse


@click.command()
@click.argument("base_conocimiento", type=click.Path(exists=True))
@click.option(
    "--script",
    type=click.Path(exists=True),
    help="Ruta del script con las instrucciones",
)
def main(base_conocimiento, script):
    """
    Asistente virtual con ollama por debajo
    """
    model = "llama3.2:3b"
    print(f"[INFO]: CARGANDO BASE DE CONOCIMIENTO.")
    messagesHistory = [
        {
            "role": "system",
            "content": "Remember this: " + " ".join(readFile(base_conocimiento)),
        },
        {
            "role": "system",
            "content": """
            You are an expert assistant in semantic networks and knowledge bases. 
            Your task is to answer questions related to RDF, SPARQL, and related concepts, 
            using the provided base as a reference.
        """,
        },
    ]
    print(f"[INFO]: CARGA REALIZADA CORRECTAMENTE.")
    print(f'[INFO]: MODELO POR DEFECTO "{model}". Para cambiar ejecute \\model')
    while True:
        try:
            query = input("> ")
            if query == "\\help":
                print(
                    """
                    Available commands:
                    \\help      - Show this help message
                    \\model     - Change the model being used
                    \\exit      - Exit the program
                    """
                )
            elif query == "\\model":
                model = input("Introduce el nombre del nuevo modelo: ")
                model = model.strip()
                print(f"Model changed to: {model}\n")
            elif query == "\\exit":
                break

            # Consulta de usuario
            messagesHistory.append(
                {
                    "role": "user",
                    "content": query,
                }
            )

            response: ChatResponse = chat(model=model, messages=messagesHistory)

            # Añadimos la respuesta de ollama al historial
            messagesHistory.append(response["message"])

            print(response["message"]["content"])
        except ollama.ResponseError as e:

            if e.status_code == 404:
                # Descarga el modelo si no lo encuentra
                print(f'[INFO]: DESCARGANDO MODELO "{model}".')
                try:
                    ollama.pull(model)
                except Exception as e:
                    print(
                        f'[OLLAMA ERROR]: ERROR AL INTENTAR DESCARGAR EL MODELO "{model}".'
                    )
            else:
                print("[OLLAMA ERROR]:", e.error)

        except Exception as e:
            print("[ERROR DURANTE EJECUCION]:", e)


if __name__ == "__main__":
    main()
