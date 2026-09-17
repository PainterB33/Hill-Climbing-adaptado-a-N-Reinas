# Hill Climbing adaptado al problema de las N-Reinas

Implementacion del algoritmo de busqueda local **Hill Climbing**, en su variante
**Steepest-Ascent con reinicios aleatorios**, para resolver el problema clasico
de las N-Reinas.

Este repositorio corresponde al taller investigativo de Introduccion a la
Inteligencia Artificial sobre algoritmos de busqueda local.

## Integrantes

- Alexander Aponte
- Thomas Arevalo
- Laura Aponte
- Sara Muñoz

## Problema

El problema de las N-Reinas consiste en ubicar N reinas en un tablero de N x N
sin que dos reinas se ataquen entre si. Una solucion valida no debe tener dos
reinas en la misma fila, columna o diagonal.

## Representacion del estado

El tablero se representa mediante un vector de longitud N:

```text
estado[columna] = fila
```

Por ejemplo, `[1, 3, 0, 2]` representa una reina en cada columna. Como el
estado inicial es una permutacion de `0` a `N - 1` y los movimientos conservan
esa permutacion, las restricciones de filas y columnas se cumplen siempre. Por
eso, la funcion de costo solo necesita contar los ataques diagonales.

## Algoritmo implementado

El archivo `hill_climbing_n_reinas.py` contiene estas partes:

- `calcular_ataques_diagonales(estado)`: calcula el numero de pares de reinas
	que se atacan diagonalmente. Un costo igual a `0` representa una solucion.
- `generar_vecinos_swap(estado)`: genera los vecinos intercambiando los
	valores de dos posiciones del vector.
- `hill_climbing_steepest_ascent(...)`: crea estados iniciales aleatorios,
	evalua todos los vecinos y se mueve al de menor costo cuando mejora el estado
	actual.
- `imprimir_tablero(estado)`: muestra el estado final en forma de tablero.

Cuando ningun vecino mejora el costo, el algoritmo considera que alcanzo un
optimo local y comienza otro reinicio aleatorio. La ejecucion termina al
encontrar costo `0` o al agotar el numero maximo de reinicios.

## Ejecucion

Desde la carpeta del proyecto se puede ejecutar:

```bash
python hill_climbing_n_reinas.py
```

La configuracion de prueba actual usa:

- `N = 8`
- hasta `100` reinicios aleatorios
- hasta `1000` movimientos por reinicio

El programa imprime el vector encontrado, el costo final, el tiempo de
ejecucion, el numero de movimientos registrados y el tablero final.