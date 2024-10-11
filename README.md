# Sistema basado en reglas capaz de realizar razonamiento hacia atrás (backward chaining), incorporando lógica difusa

Authors:
Artem Vartanov &
Mario Baldocchi

### ÍNDICE
* [Instalación y requisitos](#instalación-y-requisitos)
* [Descripción del razonamiento](#descripción-del-razonamiento)
* [Configuración avanzada](#configuración-avanzada)
* [Dependencias](#dependencias)

### Instalación y requisitos
Se requiere `python >= 3.12`

Para ejecutar el programa desde la consola de comandos

```shell
$ uv run src/practica2.py <ruta al archivo de la base de conocimiento>
```

Para probar con la base existente

```shell
$ uv run src/practica2.py base_laboral.txt
```
Al ejecutar el comando anterior aparecen las posibles acciones con las descripciones

### Descripción del razonamiento
Debajo se muestra un ejemplo del razonamiento que se aplica

Reglas
- a := b,c [0.1]
- a := d [0.4]

Hechos
- b [0.5]
- c [0.3]
- d [0.7]
```
backward_chain(a) =
or(
    and(
        and(0.5, 0.3), 
        0.1
    ),
    and(0.7, 0.4)
)
```

donde dependiendo de la configuración, descrita más abajo (por defecto min/max)
```
and(a,b) = min(a,b)
or(a,b) = max(a,b)
```
o
```
and(a,b) = a * b
or(a,b) = a + b - a * b
```
### Configuración avanzada
Para la configuración avanzada se modificaría el archivo config.toml. 
#### algorithm
Ajusta el algoritmo de razonamiento

`evaluation`: operaciones con grados de verdad, posibles valores `min/max`, `sum/prod`
#### output
Ajusta la salida del programa

`language`: idioma de la salida, posibles valores `es`, `en`

`showAppliedChain`: si el valor es `yes`, muestra la derivación al usuario.

`rangeEval`: funcion de evaluacion que imprime el texto en función del grado de verdad. Ejemplo del valor:
    
    [
        "=1 -> Si, seguro", # si es igual a 1
        ">0.8 -> Si, mucho", # si es mayor que 0.8
        "<0.3 -> No, mucho", # si es menor que 0.3
        "default -> No estoy seguro" # en cualquier otro caso
    ]

### Dependencias
Se usan los siguientes proyectos de codigo abierto:
- [uv](https://github.com/astral-sh/uv)
- [black](https://github.com/psf/black)

