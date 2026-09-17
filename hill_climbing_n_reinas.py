import random
import time
import itertools

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
    """
    mejor_estado_global = None
    mejor_costo_global = float('inf')
    
    historial_costos_global = []
    
    tiempo_inicio = time.time()

    for reinicio in range(max_reinicios):
        # Estado inicial: permutación aleatoria de 0 a N-1
        estado_actual = list(range(N))
        random.shuffle(estado_actual)
        costo_actual = calcular_ataques_diagonales(estado_actual)
        
        historial_costos_global.append(costo_actual)
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
                historial_costos_global.append(costo_actual)
                iteracion += 1
            else:
                # Nos atascamos en un óptimo local, rompemos el while para hacer un reinicio
                break
        
        # Actualizamos el mejor global encontrado hasta ahora
        if costo_actual < mejor_costo_global:
            mejor_costo_global = costo_actual
            mejor_estado_global = estado_actual
            
        # Si llegamos a costo 0, encontramos la solución perfecta y paramos
        if mejor_costo_global == 0:
            break

    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio

    return mejor_estado_global, mejor_costo_global, tiempo_ejecucion, historial_costos_global

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


# =====================================================================
# BLOQUE DE PRUEBA RÁPIDA (Borrar cuando se hagan las tablas y grafica de convergencia)
# =====================================================================
if __name__ == "__main__":
    # Declaración de hiperparámetros base
    N_reinas = 8
    reinicios = 100
    
    print(f"Iniciando Steepest-Ascent Hill Climbing para N={N_reinas}...")
    mejor_estado, mejor_costo, tiempo, historial = hill_climbing_steepest_ascent(
        N=N_reinas, 
        max_reinicios=reinicios
    )
    
    print("-" * 40)
    print(f"Vector Solución Final: {mejor_estado}")
    print(f"Costo final (Ataques diagonales): {mejor_costo}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")
    print(f"Iteraciones/movimientos registrados: {len(historial)}")
    print("-" * 40)
    
    # Imprime el tablero solo si es pequeño (N=8) para no saturar la consola
    if N_reinas <= 15:
        imprimir_tablero(mejor_estado)