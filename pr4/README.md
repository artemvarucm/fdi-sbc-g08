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

A partir de una base de conocimiento sobre la formula 1, se han generado varias bases de conocimiento, todas ellas en formato `txt`.

Quedando un dibujo tal que así:

               
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

`\temp` -  Change Ollama temperature [0, 1]. Smaller values make responses more deterministic, bigger values result in more creative responses

`\tokens` - Change Ollama maximum number of tokens for the response

`\repetition` - Change Ollama frequency_penalisation [-2, 2]. Smaller values penalise less, bigger values penalise more

`\answers` - Change Ollama number of answers

`\help` - Shows the available commands
   
`\quit` - Quit the program  


## Descripción base de datos
La base de conocimiento gira en torno a la fórmula 1.   
En ella hay información sobre distintas escuderias legendarias de esta competición: Ferrari, Mercedes, Mclaren y Aston Martin.  

Entre las distintas consultas que se le pueden hacer al sistema de conocimiento, es preciso enfatizar las relacionadas con la historia de las marcas (tanto como empresa como su equipo de formula 1), sus pilotos más reconocidos y sus modelos de coches comerciales.   
Aquí tienes algunos ejemplos:  
```
      what brand is the oldest?  
      what formula 1 driver has won more races?  
      what models has ferrari released?  
```
