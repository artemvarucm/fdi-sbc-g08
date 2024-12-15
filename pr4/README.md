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
$ uv run src/practica4.py bases mappings_ollama.json --model llama3.2:3b --explain --debug
```
--model: Specify the ollama model. By default is "llama3.2:1b"  
--explain: Enable chain of thought, explaining the steps to reach the solution
--debug: Show the context directories selected for the response (RAG)

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
`\model` -  Change Ollama model  
`\help` - Shows the available commands    
`\quit` - Quit the program  

