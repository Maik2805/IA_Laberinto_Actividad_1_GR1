import networkx as nx
import matplotlib.pyplot as plt

laberinto = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 3],
    [0, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 2, 9]
]

filas = len(laberinto)
columnas = len(laberinto[0])

# --- Construcción automática del grafo a partir de la matriz ---
G = nx.Graph()

# 1. Crear un nodo por cada celda que no sea muro (1)
for f in range(filas):
    for c in range(columnas):
        if laberinto[f][c] != 1:
            G.add_node((f, c), valor=laberinto[f][c])

# 2. Crear aristas entre celdas adyacentes (arriba/abajo/izq/der) que no sean muro
for f in range(filas):
    for c in range(columnas):
        if laberinto[f][c] == 1:
            continue  # es un muro, no tiene conexiones

        actual = (f, c)

        # Vecino de abajo
        if f + 1 < filas and laberinto[f + 1][c] != 1:
            G.add_edge(actual, (f + 1, c))

        # Vecino de la derecha
        if c + 1 < columnas and laberinto[f][c + 1] != 1:
            G.add_edge(actual, (f, c + 1))

# --- Estado inicial del jugador ---
pos = (0, 0)
coins = 30

direcciones = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1)
}

nombres_direccion = {
    "w": "arriba",
    "s": "abajo",
    "a": "izquierda",
    "d": "derecha"
}


def dibujar_grafo(pos_jugador):
    """Dibuja el grafo del laberinto usando matplotlib, marcando al jugador."""
    # Usamos la propia coordenada (fila, columna) como posición en el plano.
    # Invertimos la fila para que la matriz no se vea "boca abajo".
    posiciones = {nodo: (nodo[1], -nodo[0]) for nodo in G.nodes()}

    colores = []
    for nodo in G.nodes():
        valor = laberinto[nodo[0]][nodo[1]]
        if nodo == pos_jugador:
            colores.append("blue")       # jugador
        elif valor == 0:
            colores.append("lightgray")  # camino
        elif valor == 2:
            colores.append("orange")     # penalización
        elif valor == 3:
            colores.append("gold")       # premio
        elif valor == 9:
            colores.append("green")      # meta

    plt.figure(figsize=(8, 8))
    nx.draw(
        G,
        pos=posiciones,
        with_labels=True,
        labels={n: n for n in G.nodes()},
        node_color=colores,
        node_size=500,
        font_size=6
    )
    plt.title(f"Posición actual: {pos_jugador}")
    plt.show()


def mostrar_estado():
    print(f"\nPosición actual: {pos}  |  Monedas: {coins}")


def procesar_celda(nueva_pos):
    """Aplica el efecto de la celda a la que se acaba de mover el jugador."""
    global coins

    valor = laberinto[nueva_pos[0]][nueva_pos[1]]

    if valor == 2:
        coins -= 3
        print("¡Penalización! Pierdes 3 monedas.")
    elif valor == 0:
        coins -= 1
    elif valor == 3:
        coins -= 0.25
        print("¡Premio! Pierdes 0.25 monedas.")
    elif valor == 9:
        print("¡Has llegado a la meta!")

    return valor


def juego():
    global pos, coins

    print("=== LABERINTO ===")
    print("Controles: w = arriba, s = abajo, a = izquierda, d = derecha")
    print("Escribe 'ver' para dibujar el grafo, 'salir' para terminar la partida.\n")

    # Dibujo inicial del laberinto completo
    dibujar_grafo(pos)

    while True:
        mostrar_estado()

        if coins <= 0:
            print("Te has quedado sin monedas. Fin del juego.")
            break

        movimiento = input("Movimiento: ").strip().lower()

        if movimiento == "salir":
            print("Has salido del juego.")
            break

        if movimiento == "ver":
            dibujar_grafo(pos)
            continue

        if movimiento not in direcciones:
            print("Movimiento no válido. Usa w, s, a, d, 'ver' o 'salir'.")
            continue

        df, dc = direcciones[movimiento]
        destino = (pos[0] + df, pos[1] + dc)

        # Comprobar que el destino exista como nodo del grafo
        if not G.has_node(destino):
            print("No puedes moverte fuera del laberinto.")
            continue

        # Comprobar que exista una arista (camino libre) entre la posición
        # actual y el destino
        if G.has_edge(pos, destino):
            pos = destino
            valor = procesar_celda(pos)
            dibujar_grafo(pos)  # se actualiza el dibujo tras cada movimiento válido

            if valor == 9:
                print(f"\n¡Felicidades! Terminaste con {coins} monedas.")
                break
        else:
            print(f"No puedes moverte hacia {nombres_direccion[movimiento]}, hay un muro.")


if __name__ == "__main__":
    juego()