import click
from app import App


@click.command()
@click.argument("bases_dir", type=click.Path(exists=True))
@click.option("--model", 
    default="llama3.2:1b",
    help="Specify the ollama model. Por defecto es \"llama3.2:1b\"."
)
def main(bases_dir, model):
    """
    Asistente virtual con ollama por debajo
    """
    print("""
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
          """)
    print("WELCOME TO LOLLLAMA!\n")
    app = App(bases_dir, model)
    while True:
        try:
            query = input("> ")
            app.processCommand(query)
        except Exception as e:
            print("[RUNTIME ERROR]:", e)


if __name__ == "__main__":
    main()
