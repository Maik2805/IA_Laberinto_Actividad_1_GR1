# ==========================================================
# JUEGO DE LABERINTO USANDO UN GRAFO
# ==========================================================
# La idea principal de este programa es aprender cómo una
# matriz (el laberinto) se puede transformar en un GRAFO,
# y cómo el jugador se mueve recorriendo ese grafo (y NO
# simplemente sumando o restando a fila/columna).
# ==========================================================


# ----------------------------------------------------------
# 1. LABERINTO
# ----------------------------------------------------------
# La matriz representa el mapa del laberinto.
# 0 = camino normal
# 1 = muro (no se puede pasar)
# 2 = penalización (cuesta monedas extra)
# 3 = premio (cuesta muy pocas monedas)
# 9 = meta (llegar aquí gana el juego)

laberinto = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 3],
    [0, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 2, 9]
]


# ----------------------------------------------------------
# 2. FUNCIÓN PARA CALCULAR EL COSTO DE UNA CELDA
# ----------------------------------------------------------
def costo_celda(valor):
    """
    Recibe el valor de una celda del laberinto (0, 2, 3 o 9)
    y devuelve cuántas monedas cuesta entrar a esa celda.
    """
    if valor == 0:
        return 1          # camino normal
    elif valor == 2:
        return 3          # penalización
    elif valor == 3:
        return 0.25       # premio
    elif valor == 9:
        return 0          # meta
    else:
        return 0          # por seguridad, aunque no debería pasar


# ----------------------------------------------------------
# 3. FUNCIÓN PARA CONSTRUIR EL GRAFO A PARTIR DE LA MATRIZ
# ----------------------------------------------------------
def construir_grafo(laberinto):
    """
    Convierte la matriz del laberinto en un grafo representado
    como un diccionario de adyacencia.

    Cada celda que NO sea un muro (1) se convierte en un NODO.
    El nodo es la tupla (fila, columna).

    Luego, para cada nodo, revisamos sus 4 posibles vecinos
    (arriba, abajo, izquierda, derecha). Si el vecino existe
    dentro de la matriz y tampoco es un muro, se crea una
    conexión (arista) usando la letra del movimiento como clave:
        "w" = arriba
        "s" = abajo
        "a" = izquierda
        "d" = derecha
    """

    grafo = {}  # aquí se guardará el diccionario de adyacencia

    filas = len(laberinto)
    columnas = len(laberinto[0])

    # Recorremos toda la matriz celda por celda
    for f in range(filas):
        for c in range(columnas):

            # Si la celda es un muro, la ignoramos: no se
            # convierte en nodo y no puede tener conexiones.
            if laberinto[f][c] == 1:
                continue

            nodo_actual = (f, c)

            # Creamos el nodo en el grafo (si no existe aún)
            if nodo_actual not in grafo:
                grafo[nodo_actual] = {}

            # Lista de posibles movimientos:
            # (letra del movimiento, fila destino, columna destino)
            movimientos = [
                ("w", f - 1, c),   # arriba
                ("s", f + 1, c),   # abajo
                ("a", f, c - 1),   # izquierda
                ("d", f, c + 1),   # derecha
            ]

            for letra, nf, nc in movimientos:
                # Comprobamos que el vecino esté dentro de la matriz
                dentro_del_mapa = 0 <= nf < filas and 0 <= nc < columnas

                if dentro_del_mapa:
                    # Comprobamos que el vecino no sea un muro
                    if laberinto[nf][nc] != 1:
                        # Creamos la conexión (arista) entre
                        # el nodo actual y el nodo vecino
                        grafo[nodo_actual][letra] = (nf, nc)

    return grafo


# ----------------------------------------------------------
# 4. FUNCIÓN PARA MOSTRAR EL TABLERO
# ----------------------------------------------------------
def imprimir_tablero(lab, pos, coins):
    """
    Imprime el laberinto en la terminal, mostrando un 8 en
    la posición actual del jugador.
    """
    print()
    for f in range(len(lab)):
        fila_mostrar = []
        for c in range(len(lab[0])):
            if (f, c) == pos:
                fila_mostrar.append(8)   # aquí está el jugador
            else:
                fila_mostrar.append(lab[f][c])
        print(fila_mostrar)
    print(f"\nMonedas actuales: {coins}")


# ----------------------------------------------------------
# 5. CONSTRUIR EL GRAFO A PARTIR DEL LABERINTO
# ----------------------------------------------------------
grafo = construir_grafo(laberinto)

# Mostramos un ejemplo real de cómo quedó el grafo,
# para entender la conversión matriz -> grafo.
print("Ejemplo de nodos generados en el grafo:")
print("(0, 0) ->", grafo[(0, 0)])
print("(2, 3) ->", grafo.get((2, 3), "este nodo no existe (es un muro)"))
print()


# ----------------------------------------------------------
# 6. INICIALIZAR JUGADOR Y MONEDAS
# ----------------------------------------------------------
pos = (0, 0)
coins = 30


# ----------------------------------------------------------
# 7. BUCLE PRINCIPAL DEL JUEGO
# ----------------------------------------------------------
imprimir_tablero(laberinto, pos, coins)

while True:
    movimiento = input("\nMueve con W/A/S/D: ").lower().strip()

    # Validamos que la tecla sea una de las permitidas
    if movimiento not in ("w", "a", "s", "d"):
        print("❌ Movimiento inválido")
        continue

    # Consultamos el grafo para ver si existe una conexión
    # desde la posición actual usando esa letra.
    conexiones = grafo[pos]

    if movimiento not in conexiones:
        print("🚧 No puedes moverte en esa dirección")
        continue

    # Si la conexión existe, obtenemos el nodo vecino.
    # AQUÍ es donde el jugador se mueve usando el GRAFO,
    # y no modificando fila/columna directamente.
    nueva_pos = conexiones[movimiento]

    # Calculamos el costo de entrar a la nueva celda
    valor_celda = laberinto[nueva_pos[0]][nueva_pos[1]]
    costo = costo_celda(valor_celda)

    # Actualizamos monedas y posición
    coins -= costo
    pos = nueva_pos

    # Mostramos el tablero actualizado
    imprimir_tablero(laberinto, pos, coins)

    # Comprobamos condiciones de victoria o derrota
    if valor_celda == 9:
        print("\n🎉 ¡Llegaste a la meta! ¡Ganaste! 🎉")
        break

    if coins <= 0:
        print("\n💀 Te quedaste sin monedas. ¡Perdiste! 💀")
        break