# Sistema que permite representar y consultar redes semánticas usando un subconjunto simplificado de RDF y SPARQL partiendo de la base de conocimiento

Authors:
Artem Vartanov &
Mario Baldocchi

### ÍNDICE
* [Instalación y requisitos](#instalación-y-requisitos)
* [Ejecución del programa](#instalación-y-requisitos)
* [Descripción programa](#descripción-programa)
* [Dependencias](#dependencias)

## Instalación y requisitos
Se requiere 

- [`python >= 3.12`](https://www.python.org/downloads/#:~:text=%EE%80%80Python.org%EE%80%81%20offers%20downloads%20for%20Python)
- [black](https://pypi.org/project/black/)
- [click](https://pypi.org/project/click/) 
- [`ollama`](https://pypi.org/project/uv/)
- [`uv`](https://pypi.org/project/uv/)



## Ejecución del programa
### Base:
```shell
$ uv run src/practica4.py
```
### Avanzada:
```shell
$ uv run src/practica4.py --model --explain
```
--model: Specify the ollama model. By default is "llama3.2:1b"  
--explain: Enable chain of thought, explaining the steps to reach the solution


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
`\\model` -  Change Ollama model  
`\\help` - Shows the available commands    
`\\quit` - Quit the program  
`\\add <file_name> <file_path>` - Adds a new knowledge base (`.txt`)


