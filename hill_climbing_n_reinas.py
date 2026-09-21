import random
import time
import itertools
import argparse
import matplotlib
matplotlib.use("Agg")  # permite generar la imagen sin necesidad de una ventana gráfica
import matplotlib.pyplot as plt

def calcular_ataques_diagonales(estado):
    """
    Función de costo: Cuenta el número de ataques en las diagonales.
    Un costo de 0 significa que es una solución óptima.
    """
    ataques = 0
    n = len(estado)
    # Se evalúan todas las parejas posibles de reinas
    for i in range(n):
        for j in range(i + 1, n):
            # Hay ataque diagonal si la distancia en columnas es igual a la distancia en filas
            if abs(i - j) == abs(estado[i] - estado[j]):
                ataques += 1
    return ataques

def generar_vecinos_swap(estado):
    """
    Operador de vecindario: Genera todos los vecinos posibles intercambiando 
    (swap) los valores de dos posiciones del vector.
    """
    vecinos = []
    n = len(estado)
    # itertools.combinations genera todos los pares de índices (i, j) sin repetir
    for i, j in itertools.combinations(range(n), 2):
        nuevo_estado = list(estado)
        # Se realiza el swap
        nuevo_estado[i], nuevo_estado[j] = nuevo_estado[j], nuevo_estado[i]
        vecinos.append(nuevo_estado)
    return vecinos

def hill_climbing_steepest_ascent(N, max_reinicios=100, max_iteraciones=1000):
    """
    Algoritmo principal: Steepest-Ascent Hill Climbing con reinicios aleatorios.

    Devuelve además métricas para el reporte del taller:
    - historial_convergencia: evolución del costo SOLO del reinicio que
      produjo la mejor solución (sirve para la gráfica de convergencia).
    - reinicios_usados / iteraciones_usadas: para reportar cuánto costó
      llegar a la solución.
    """
    mejor_estado_global = None
    mejor_costo_global = float('inf')
    historial_convergencia = []

    reinicios_usados = 0
    iteraciones_usadas = 0

    tiempo_inicio = time.time()

    for reinicio in range(max_reinicios):
        reinicios_usados = reinicio + 1

        # Estado inicial: permutación aleatoria de 0 a N-1
        estado_actual = list(range(N))
        random.shuffle(estado_actual)
        costo_actual = calcular_ataques_diagonales(estado_actual)

        historial_este_reinicio = [costo_actual]
        iteracion = 0

        # Ciclo de Hill Climbing
        while costo_actual > 0 and iteracion < max_iteraciones:
            vecinos = generar_vecinos_swap(estado_actual)

            # Estrategia Steepest-Ascent: buscar el MEJOR vecino de todos
            mejor_vecino = None
            mejor_costo_vecino = float('inf')

            for vecino in vecinos:
                costo_vecino = calcular_ataques_diagonales(vecino)
                if costo_vecino < mejor_costo_vecino:
                    mejor_costo_vecino = costo_vecino
                    mejor_vecino = vecino

            # Si el mejor vecino mejora la solución actual, nos movemos a él
            if mejor_costo_vecino < costo_actual:
                estado_actual = mejor_vecino
                costo_actual = mejor_costo_vecino
                historial_este_reinicio.append(costo_actual)
                iteracion += 1
            else:
                # Nos atascamos en un óptimo local, rompemos el while para hacer un reinicio
                break

        # Actualizamos el mejor global encontrado hasta ahora
        if costo_actual < mejor_costo_global:
            mejor_costo_global = costo_actual
            mejor_estado_global = estado_actual
            historial_convergencia = historial_este_reinicio
            iteraciones_usadas = iteracion

        # Si llegamos a costo 0, encontramos la solución perfecta y paramos
        if mejor_costo_global == 0:
            break

    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio

    return {
        "N": N,
        "estado": mejor_estado_global,
        "costo": mejor_costo_global,
        "tiempo": tiempo_ejecucion,
        "historial_convergencia": historial_convergencia,
        "reinicios_usados": reinicios_usados,
        "iteraciones_usadas": iteraciones_usadas,
    }

def imprimir_tablero(estado):
    """
    Función de utilidad para visualizar el tablero final.
    """
    N = len(estado)
    print("\nTablero final:")
    for fila in range(N):
        fila_str = ""
        for col in range(N):
            # Si el valor en la columna actual es igual a la fila, hay una reina
            if estado[col] == fila:
                fila_str += "[Q]"
            else:
                fila_str += "[ ]"
        print(fila_str)

def graficar_tablero(estado, ruta_salida="tablero.png"):
    """
    Dibuja el tablero final con matplotlib (casillas tipo ajedrez + reinas).
    Sirve para cualquier N, incluyendo N grandes donde la versión de texto
    ya no es legible.
    """
    N = len(estado)
 
    fig, eje = plt.subplots(figsize=(6, 6))
 
    # Dibuja las casillas alternando colores, como un tablero de ajedrez
    tablero_colores = [[(fila + col) % 2 for col in range(N)] for fila in range(N)]
    eje.imshow(tablero_colores, cmap="Greys", vmin=0, vmax=1.5)
 
    # Dibuja una reina en cada columna, en la fila indicada por el vector solución
    for columna, fila in enumerate(estado):
        eje.text(columna, fila, "♛", fontsize=max(6, 200 // N),
                  ha="center", va="center", color="red")
 
    eje.set_title(f"Tablero final — N={N}")
    eje.set_xticks(range(N))
    eje.set_yticks(range(N))
    # Con N grande, ocultar las etiquetas de los ejes para que no se amontonen
    if N > 20:
        eje.set_xticklabels([])
        eje.set_yticklabels([])
    eje.set_xlabel("Columna")
    eje.set_ylabel("Fila")
 
    fig.tight_layout()
    fig.savefig(ruta_salida, dpi=150)
    plt.close(fig)
    print(f"Tablero final guardado en: {ruta_salida}")

def imprimir_metricas(resultado):
    """
    Imprime las métricas de la corrida: vector solución, costo final
    (ataques diagonales) y tiempo de ejecución en segundos.
    """
    print("\n" + "-" * 40)
    print(f"Vector Solución Final: {resultado['estado']}")
    print(f"Costo final (Ataques diagonales): {resultado['costo']}")
    print(f"Tiempo de ejecución: {resultado['tiempo']:.4f} segundos")
    print(f"Reinicios usados: {resultado['reinicios_usados']}  |  "
          f"Iteraciones del reinicio ganador: {resultado['iteraciones_usadas']}")
    print("-" * 40)


def graficar_convergencia(resultado, ruta_salida="convergencia.png"):
    """
    Grafica cómo disminuyó el costo (ataques diagonales) a lo largo de las
    iteraciones del reinicio que llegó a la mejor solución.
    Guarda la imagen en la ruta especificada.
    """
    historial = resultado["historial_convergencia"]

    fig, eje = plt.subplots(figsize=(7, 4))
    eje.plot(range(len(historial)), historial, marker="o", markersize=3)
    eje.set_title(f"Convergencia — N={resultado['N']}")
    eje.set_xlabel("Iteración")
    eje.set_ylabel("Costo (ataques diagonales)")
    eje.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()
    fig.savefig(ruta_salida, dpi=150)
    plt.close(fig)
    print(f"\nGráfica de convergencia guardada en: {ruta_salida}")


# =====================================================================
# BLOQUE PRINCIPAL: ejecuta el algoritmo para un N dado y genera
# los 3 entregables de la sección "Visualización y Métricas":
#   1. Tablero final / vector solución
#   2. Costo final y tiempo de ejecución
#   3. Gráfica de convergencia
# =====================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Hill Climbing aplicado al problema de las N-Reinas"
    )
    parser.add_argument(
        "N_REINAS",
        type=int,
        help="Cantidad de reinas y tamaño del tablero"
    )
    args = parser.parse_args()

    N_REINAS = args.N_REINAS
    MAX_REINICIOS = 100
    MAX_ITERACIONES = 1000
    SEMILLA_ALEATORIA = 42

    random.seed(SEMILLA_ALEATORIA)

    print(f"Ejecutando Steepest-Ascent Hill Climbing para N={N_REINAS}...")
    resultado = hill_climbing_steepest_ascent(
        N=N_REINAS,
        max_reinicios=MAX_REINICIOS,
        max_iteraciones=MAX_ITERACIONES,
    )

    imprimir_tablero(resultado["estado"])
    graficar_tablero(resultado["estado"])
    imprimir_metricas(resultado)
    graficar_convergencia(resultado)