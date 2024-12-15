# LOLLLAMA: Asistente virtual para un ingeniero de conocimiento basado en Ollama

Authors:
Artem Vartanov &
Mario Baldocchi

### ÍNDICE
* [Instalación y requisitos](#instalación-y-requisitos)
* [Ejecución del programa](#ejecución-del-programa)
* [Descripción programa](#descripción-programa)

## Instalación y requisitos
Se requiere 

- [`python >= 3.12`](https://www.python.org/downloads/#:~:text=%EE%80%80Python.org%EE%80%81%20offers%20downloads%20for%20Python)
- [black](https://pypi.org/project/black/)
- [click](https://pypi.org/project/click/) 
- [`ollama`](https://pypi.org/project/ollama/)
- [`autocorrect`](https://pypi.org/project/autocorrect/)


## Ejecución del programa
### Base:
```shell
$ uv run src/practica4.py bases mappings_ollama.json
```
### Avanzada:
```shell
$ uv run src/practica4.py bases mappings_ollama.json --model llama3.2:3b --temperature 0.8 --explain --debug
```

bases is the knowledge directory path, mappings_ollama.json is the path to JSON with RAG mappings.

`--model`: Specify the ollama model. By default is "llama3.2:1b"

`--temperature`: Set the randomness of the model's responses. Smaller values make responses more deterministic, bigger values result in more creative responses. Default is 0.7

`--explain`: Enable chain of thought, explaining the steps to reach the solution

`--debug`: Print the context directories selected (filtered) for the response (RAG)

## Descripción programa
* [General](#general)  
* [Comandos](#comandos)  

### General
Este programa está diseñado para procesar lenguaje natural, permitiendo la interacción con el usuario a través de un chat. Además, se enfoca en gestionar bases de conocimiento escritas en lenguaje natural.

Por un lado, cuenta con una base de conocimiento principal en formato `txt`, y a partir de esta, se generan otras bases de conocimiento adicionales, también en formato `txt`.

Quedando, por ejemplo, un dibujo tal que así:

               
```markdown
base_principal
  │  
  ├── base_secundaria_1
  │      
  ├── base_secundaria_2
  │   
  └── base_secundaria_3  
```

### Comandos
`\status` - Shows current program settings

`\model` -  Change Ollama model  

`\temp` -  Change Ollama temperature. Smaller values (< 0.5) make responses more deterministic, bigger values (> 1.0) result in more creative responses

`\help` - Shows the available commands
   
`\quit` - Quit the program  

