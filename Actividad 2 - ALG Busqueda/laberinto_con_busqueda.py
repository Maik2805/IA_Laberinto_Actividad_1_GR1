import networkx as nx
import matplotlib.pyplot as plt

# 0 = camino libre, 1 = pared, 9 = meta
laberinto = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 9, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0]
]

filas = len(laberinto)
columnas = len(laberinto[0])

# Detectar inicio y meta dinámicamente desde la matriz
# El inicio siempre es (0, 0); la meta es la celda con valor 9
INICIO = (0, 0)
META = next(
    (f, c)
    for f in range(filas)
    for c in range(columnas)
    if laberinto[f][c] == 9
)

# --- Construcción automática del grafo a partir de la matriz ---
G = nx.Graph()

# Crear un nodo por cada celda que no sea muro (1)
for f in range(filas):
    for c in range(columnas):
        if laberinto[f][c] != 1:
            G.add_node((f, c), valor=laberinto[f][c])

# Crear aristas entre celdas adyacentes (arriba/abajo/izq/der) que no sean muro
for f in range(filas):
    for c in range(columnas):
        if laberinto[f][c] == 1:
            continue

        actual = (f, c)

        # Vecino de abajo
        if f + 1 < filas and laberinto[f + 1][c] != 1:
            G.add_edge(actual, (f + 1, c))

        # Vecino de la derecha
        if c + 1 < columnas and laberinto[f][c + 1] != 1:
            G.add_edge(actual, (f, c + 1))


# ---------------------------------------------------------------------------
# ALGORITMOS DE BÚSQUEDA
# ---------------------------------------------------------------------------

def bfs(grafo, inicio, objetivo):
    """
    Búsqueda en Anchura (BFS).
    Usa una cola FIFO (pop(0)) para explorar nivel por nivel.
    Garantiza el camino con menor número de pasos.
    """
    cola = [inicio]
    visitados = {inicio}           # conjunto de nodos ya procesados
    predecesor = {inicio: None}    # para reconstruir el camino
    orden_visita = [inicio]        # registro del orden de exploración

    while cola:
        nodo = cola.pop(0)         # FIFO: extrae el primero

        if nodo == objetivo:
            # Reconstrucción del camino desde meta hasta inicio
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = predecesor[nodo]
            return list(reversed(camino)), orden_visita

        for vecino in grafo.neighbors(nodo):
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                cola.append(vecino)
                orden_visita.append(vecino)

    return None, orden_visita  # no se encontró camino


def dfs(grafo, inicio, objetivo):
    """
    Búsqueda en Profundidad (DFS).
    Usa una pila LIFO (pop(-1)) para explorar rama a rama.
    No garantiza el camino más corto.
    """
    pila = [inicio]
    visitados = {inicio}           # conjunto de nodos ya procesados
    predecesor = {inicio: None}    # para reconstruir el camino
    orden_visita = [inicio]        # registro del orden de exploración

    while pila:
        nodo = pila.pop(-1)        # LIFO: extrae el último

        if nodo == objetivo:
            # Reconstrucción del camino desde meta hasta inicio
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = predecesor[nodo]
            return list(reversed(camino)), orden_visita

        for vecino in grafo.neighbors(nodo):
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                pila.append(vecino)
                orden_visita.append(vecino)

    return None, orden_visita  # no se encontró camino


# ---------------------------------------------------------------------------
# VISUALIZACIÓN
# ---------------------------------------------------------------------------

POS_GRAFO = {nodo: (nodo[1], -nodo[0]) for nodo in G.nodes()}


def dibujar_laberinto_inicial():
    """Muestra el grafo del laberinto sin ningún recorrido aplicado."""
    colores = []
    for nodo in G.nodes():
        if nodo == INICIO:
            colores.append("orange")     # inicio
        elif laberinto[nodo[0]][nodo[1]] == 9:
            colores.append("green")      # meta
        else:
            colores.append("lightgray")  # camino libre

    fig = plt.figure(figsize=(9, 9))
    nx.draw(
        G,
        pos=POS_GRAFO,
        with_labels=True,
        labels={n: n for n in G.nodes()},
        node_color=colores,
        node_size=500,
        font_size=6
    )
    fig.text(0.5, 0.97, "Laberinto — Estado inicial",
             ha="center", va="top", fontsize=11, fontweight="bold")
    fig.text(0.5, 0.93, "Naranja: inicio  |  Verde: meta",
             ha="center", va="top", fontsize=9)
    fig.text(0.5, 0.01, "Cierra esta ventana para elegir el algoritmo",
             ha="center", va="bottom", fontsize=9,
             color="white", backgroundcolor="steelblue",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="steelblue", edgecolor="none"))
    plt.show()


def dibujar_resultado(algoritmo, camino, visitados):
    """
    Pinta el grafo con el resultado de la búsqueda:
      - Azul claro : nodos visitados durante la exploración
      - Verde      : nodos que forman la ruta encontrada
      - Naranja    : inicio
      - Rojo       : meta
    """
    conjunto_ruta = set(camino) if camino else set()

    colores = []
    for nodo in G.nodes():
        if nodo in conjunto_ruta:
            if nodo == INICIO:
                colores.append("orange")   # inicio (parte de la ruta)
            elif nodo == META:
                colores.append("red")      # meta alcanzada
            else:
                colores.append("limegreen")  # ruta óptima
        elif nodo in visitados:
            colores.append("steelblue")    # explorado pero fuera de la ruta
        else:
            colores.append("lightgray")    # no visitado

    # Resaltar las aristas que forman la ruta
    aristas_ruta = []
    if camino:
        aristas_ruta = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]

    aristas_color = [
        "limegreen" if (u, v) in aristas_ruta or (v, u) in aristas_ruta else "lightgray"
        for u, v in G.edges()
    ]
    aristas_ancho = [
        3.0 if (u, v) in aristas_ruta or (v, u) in aristas_ruta else 1.0
        for u, v in G.edges()
    ]

    pasos_ruta = len(camino) - 1 if camino else 0
    titulo = (
        f"Algoritmo: {algoritmo}  |  "
        f"Nodos explorados: {len(visitados)}  |  "
        f"Pasos en la ruta: {pasos_ruta}"
    )
    if not camino:
        titulo += "  |  ⚠ No se encontró camino"

    fig = plt.figure(figsize=(9, 9))
    nx.draw(
        G,
        pos=POS_GRAFO,
        with_labels=True,
        labels={n: n for n in G.nodes()},
        node_color=colores,
        edge_color=aristas_color,
        width=aristas_ancho,
        node_size=500,
        font_size=6
    )
    fig.text(0.5, 0.97, titulo,
             ha="center", va="top", fontsize=9, fontweight="bold")
    fig.text(0.5, 0.01, "Cierra esta ventana para continuar",
             ha="center", va="bottom", fontsize=9,
             color="white",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="steelblue", edgecolor="none"))
    plt.show()


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    print("=" * 45)
    print("       LABERINTO — BÚSQUEDA AUTOMÁTICA")
    print("=" * 45)
    print(f"  Inicio : {INICIO}")
    print(f"  Meta   : {META}")
    print(f"  Nodos  : {G.number_of_nodes()}  |  Aristas: {G.number_of_edges()}")
    print("=" * 45)

    # Mostrar el laberinto antes de resolver
    print("\nMostrando el laberinto inicial...")
    dibujar_laberinto_inicial()

    # Selección del algoritmo
    print("\n¿Con qué algoritmo deseas resolverlo?")
    print("  (1) BFS — Búsqueda en Anchura")
    print("  (2) DFS — Búsqueda en Profundidad")
    print("  (0) Salir del programa")

    while True:
        opcion = input("\nIngresa 1 o 2: ").strip()
        if opcion in ("1", "2"):
            break
        if opcion == "0":
            return
        print("  Opción no válida, ingresa 1 o 2.")

    if opcion == "1":
        nombre = "BFS"
        camino, visitados = bfs(G, INICIO, META)
    else:
        nombre = "DFS"
        camino, visitados = dfs(G, INICIO, META)

    # Mostrar resultados en consola
    print(f"\n--- Resultado {nombre} ---")
    if camino:
        print(f"  Ruta encontrada ({len(camino) - 1} pasos):")
        print(f"  {' → '.join(str(n) for n in camino)}")
    else:
        print("  No se encontró un camino hacia la meta.")

    print(f"  Nodos explorados: {len(visitados)}")
    print(f"  Orden de exploración: {visitados}")

    # Mostrar resultado visual
    print("\nMostrando resultado visual...")
    print("  Azul   = nodos explorados")
    print("  Verde  = ruta encontrada")
    print("  Naranja = inicio  |  Rojo = meta")
    dibujar_resultado(nombre, camino, set(visitados))


if __name__ == "__main__":
    main()
