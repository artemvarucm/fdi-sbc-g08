import click
from app import App


@click.command()
@click.argument("bases_dir", type=click.Path(exists=True))
@click.argument("mappings", type=click.Path(exists=True))
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
def main(bases_dir, mappings, model, explain):
    """
    Asistente virtual con ollama por debajo
    """
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
    app = App(bases_dir, mappings, model, explain)
    while True:
        try:
            query = input("> ")
            app.processCommand(query)
        except Exception as e:
            print("[RUNTIME ERROR]:", e)


if __name__ == "__main__":
    main()
