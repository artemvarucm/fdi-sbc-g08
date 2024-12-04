import sys
import click
from utils import readFile
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
    Programa que permite representar y consultar redes semánticas
    usando un subconjunto simplificado de RDF y SPARQL partiendo de la base de conocimiento
    """

    try:
        while True:
            query = input("> ")
            response: ChatResponse = chat(model='llama3.2:3b', messages=[
            {
                'role': 'system',
                'content': 'Remember this: ' + " ".join(readFile(base_conocimiento)),
            },
            {
                'role': 'user',
                'content': query,
            },
            ])
            print(response['message']['content'])
            # or access fields directly from the response object
            #print(response.message.content)
    except Exception as e:
        print("[ERROR DURANTE EJECUCION]:", e)


if __name__ == "__main__":
    main()
