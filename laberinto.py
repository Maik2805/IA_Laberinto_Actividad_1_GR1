import os
import msvcrt

# ── Tipos de celda ──────────────────────────────────────────────
LIBRE        = "LIBRE"
JUGADOR      = "JUGADOR"
META         = "META"
PARED        = "PARED"
PENAL = "PENAL"
PREMI       = "PREMI"


# Definicion uso de coins:
COSTO_BASE = 4
COINS_TOTALES = COSTO_BASE * 22

COSTOS = {
        LIBRE: COSTO_BASE,
        PREMI: COSTO_BASE / 4,
        PENAL: COSTO_BASE * 3 ,
        META: COSTO_BASE,
    }

DIRS = {
        b"w": (-1,  0),
        b"s": ( 1,  0),
        b"a": ( 0, -1),
        b"d": ( 0,  1),
    }

SIMBOLOS = {
    LIBRE:        " ",
    JUGADOR:      "O",
    META:         "M",
    PARED:        "X",
    PENAL:        "☢︎",
    PREMI:        "✔︎",
}

# Construcción del mapa como grilla para facilitar la configuración:
# Cada fila es una lista de tipos de celda.
# Inicio del jugador: (0, 0)   Meta: (8, 8)
MAPA = [
    [LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED, LIBRE, LIBRE],  # fila 0
    [PARED, LIBRE, PARED, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED],  # fila 1
    [LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE, PARED, LIBRE, LIBRE],  # fila 2
    [LIBRE, PARED, PARED, LIBRE, LIBRE, LIBRE, LIBRE, PARED, LIBRE],  # fila 3
    [LIBRE, LIBRE, LIBRE, PARED, PENAL, PARED, LIBRE, LIBRE, LIBRE],  # fila 4
    [PARED, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED, LIBRE, PARED],  # fila 5
    [LIBRE, LIBRE, LIBRE, PARED, PREMI, LIBRE, LIBRE, LIBRE, LIBRE], # fila 6
    [LIBRE, PARED, LIBRE, LIBRE, PARED, LIBRE, PARED, PARED, LIBRE],  # fila 7
    [LIBRE, LIBRE, PARED, LIBRE, LIBRE, LIBRE, PARED, LIBRE, META ],  # fila 8
]

# Grafo: lista de vecinos para cada celda (nodo)
# Solo se conectan celdas que NO son PARED, en las 4 direcciones.
def construir_grafo():
    grafo = {}
    filas    = len(MAPA)
    columnas = len(MAPA[0])

    for f in range(filas):
        for c in range(columnas):
            if MAPA[f][c] == PARED:
                continue
            vecinos = []
            for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nf, nc = f+df, c+dc
                if 0 <= nf < filas and 0 <= nc < columnas:
                    if MAPA[nf][nc] != PARED:
                        vecinos.append((nf, nc))
            grafo[(f, c)] = vecinos

    return grafo

# Imprime el grafo construido a partir del mapa, como evidencia de su construcción.
# Muestra cada nodo con su tipo y la lista de nodos vecinos.
# Los nodos se identifican como (fila, columna).
def imprimir_grafo(grafo):
    print("=" * 60)
    print("  GRAFO DEL LABERINTO  (nodo -> vecinos conectados)")
    print("=" * 60)
    print(f"  {'Nodo':<12} {'Tipo':<14} {'Vecinos'}")
    print("-" * 60)
    for f in range(9):
        for c in range(9):
            nodo = (f, c)
            if nodo not in grafo:
                continue
            tipo    = MAPA[f][c]
            vecinos = grafo[nodo]
            vecinos_str = "  ".join(str(v) for v in vecinos)
            print(f"  {str(nodo):<12} {tipo:<14} {vecinos_str}")
    print("=" * 60)
    print(f"  Total nodos transitables: {len(grafo)}")
    print("=" * 60)
    input("\n  Presiona Enter para iniciar el juego...")

# Imprimir en la terminal el mapa luego de cada movimiento
def imprimir_mapa(pos, coins):
    os.system("cls")
    f_j, c_j = pos

    print("+" + "---+" * 9)
    for f in range(9):
        fila = "|"
        for c in range(9):
            if (f, c) == (f_j, c_j):
                simbolo = SIMBOLOS[JUGADOR]
            else:
                simbolo = SIMBOLOS[MAPA[f][c]]
            fila += f" {simbolo} |"
        print(fila)
        print("+" + "---+" * 9)

    print(f"\nCoins: {coins} | Movimiento: {COSTO_BASE} | {SIMBOLOS['PREMI']} {COSTOS['PREMI']} | {SIMBOLOS['PENAL']}: {COSTOS['PENAL']} ")

def jugar():
    grafo  = construir_grafo()
    pos    = (0, 0)
    coins  = COINS_TOTALES

    imprimir_grafo(grafo)

    imprimir_mapa(pos, coins)
    print("Llega a M conservando coins  |  w/a/s/d para moverte  |  q para salir")

    while True:
        tecla = msvcrt.getch().lower()

        if tecla == b"q":
            print("Saliendo...")
            break

        if tecla not in DIRS:
            continue

        df, dc = DIRS[tecla]
        destino = (pos[0]+df, pos[1]+dc)

        # Verificar que el destino sea un nodo valido y esté conectado con el nodo de la posición actual del jugador [pos]
        if destino not in grafo or destino not in grafo[pos]:
            imprimir_mapa(pos, coins)
            print("No puedes ir en esa direccion (pared o limite).")
            continue

        tipo_destino = MAPA[destino[0]][destino[1]]
        costo = COSTOS[tipo_destino]

        if coins - costo < 0:
            imprimir_mapa(pos, coins)
            print(f"Sin coins suficientes (necesitas {costo}, tienes {coins}).")
            continue

        pos    = destino
        coins -= costo

        imprimir_mapa(pos, coins)

        if pos == (8, 8):
            print(f"¡Ganaste! Llegaste a la meta con {coins} coins.")
            break

        if coins == 0:
            print("¡Sin coins! Perdiste.")
            break

        tipo = MAPA[pos[0]][pos[1]]
        if tipo == PENAL:
            print(f"{SIMBOLOS['PENAL']}  Celda de PENALIZACIÓN: costo triple.")
        elif tipo == PREMI:
            print(f"{SIMBOLOS['PREMI']}  Celda de PREMIO: costo minimo.")
        else:
            print("w/a/s/d para moverte  |  q para salir")

if __name__ == "__main__":
    jugar()
