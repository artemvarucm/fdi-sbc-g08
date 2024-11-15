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
Se requiere `python >= 3.12`


## Ejecución del programa
**-Sin script de comandos**

```shell
$ uv run src/practica3.py <ruta al archivo de la base de conocimiento>
```
**-Con script de comandos**

```shell
$ uv run src/practica3.py <ruta al archivo de la base de conocimiento> --script <ruta al archivo de comandos>
```
## Descripción programa
* [General](#general)  
* [Comandos](#comandos)  
* [Notas importantes](#notas-importantes)  

### General
Este programa se centra en el manejo de bases de conocimiento. 

Las bases de conocimiento deben contener la información siguiendo el marco RDF (Resource Description Framework),
tal y como se indica en el siguiente esquema:

```sparql
q\d:sujeto t\d:predicado q\d:objeto ;
       t\d:predicado2 q\d:objeto2 ;
       t\d:predicado3 q\d:objeto3 .
```

### Comandos
`load <base_conocimiento>` - añadir base de conocimiento desde el archivo <base_conocimiento>  
`add <afirmación>` - añadir una afirmación a la base de conocimiento  
`save "<base_conocimiento>"` - guardar la base de conocimiento en el archivo <base_conocimiento>  
`draw "<imagen>"` - muestra la última consulta con grafos. Guarda el png en el archivo <imagen>  
`select "<consulta>"` - devuelve en formato tabla el resultado de la consulta
`help` - muestra los comandos del programa  
`quit` - salir del programa  
`Ctrl+C` - salir del programa o salir del modo multilinea (select, add)  

### Notas importantes
* [Notación](#notacin)  
  * [Wikidata](#wikidata)
  * [Valores literales](#valores-literales)  
* [Sinónimos](#sinnimos)
* [Extensión bases de conocimiento](#extensin-bases-de-conocimiento)


#### Notación
#### Wikidata
Se pueden usar elementos de wikidata con los
prefijos wd: y wdt:. Por ejemplo 
```sparql
q8:El_matador wdt:P31 q8:persona .
```
#### Valores literales
Los valores literales para atributos se escribirán entre comillas dobles
```sparql
q8:El_matador wdt:P31 q8:persona ;
              t8:nombre "Ilia" ;
```

#### Sinónimos
El programa "entiende" sinónimos mediante la propiedad [wdt:P1628](https://www.wikidata.org/wiki/Property:P1628)  
El establecimiento de sinónimos se hace de la siguiente manera:
```sparql
t1:matriculado wdt:P1628 t2:participante .
```

#### Extensión bases de conocimiento
La extensión de los archivos que contengan la base de conocimiento debe ser .ttl ó .txt

## Dependencias
Se usan los siguientes proyectos de codigo abierto:
- [uv](https://pypi.org/project/uv/)
- [black](https://pypi.org/project/black/)
- [click](https://pypi.org/project/click/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [networkx](https://pypi.org/project/networkx/)
- [pandas](https://pypi.org/project/pandas/)
- [tabulate](https://pypi.org/project/tabulate/)


