import click
import sys
from app import App


@click.command()
@click.argument("bases_dir", type=click.Path(exists=True))
@click.argument("mappings_json", type=click.Path(exists=True))
@click.option(
    "--model",
    default="llama3.2:1b",
    help='Specify the ollama model. By default is "llama3.2:1b".',
)
@click.option(
    "--explain",
    is_flag=True,
    help="Enable chain of thought, explaining the steps to reach the solution.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Print the context directories selected (filtered) for the response (RAG)",
)
def main(bases_dir, mappings_json, model, temperature, explain, debug):
    """
    Virtual Assistant based on Ollama. BASES_DIR is the knowledge directory path, MAPPINGS_JSON is the path to JSON with RAG mappings.
    """
    try:
        app = App(bases_dir, mappings_json, model, temperature, explain, debug)
    except Exception as e:
        print(e)
        sys.exit(1)

    print(
        """
          __
       .-'  `'.
      /        \\
     ; .-"``"-. ;
     |/  _  _  \\|
     (   (o)(o)  )
     |    .--.   | 
     |   |\\__/|  | 
     |           |  
     |           |   
    /             \\   
   ;   ________   ;   
  /   /        \\  \\   
  |  /          \\  \\  
  | |            | | 
  | |            | | 
  | |            | | 
  |_|            |_|
  (__)           (__)
          """
    )
    print("WELCOME TO LOLLLAMA!\n")
    while True:
        try:
            query = input("> ")
            app.processCommand(query)
        except Exception as e:
            print("[RUNTIME ERROR]:", e)


if __name__ == "__main__":
    main()
