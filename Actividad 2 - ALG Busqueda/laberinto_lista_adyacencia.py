"""
Laberinto resuelto con BFS, DFS y UCS usando una LISTA DE ADYACENCIA explícita.

El grafo representa EXACTAMENTE el laberinto de la versión por matriz
(laberinto_con_busqueda.py), pero aquí cada arista lleva su COSTO escrito de
forma explícita en el diccionario. Así puedes modificar cualquier costo a mano
sin tener que derivarlo del tipo de celda.

    grafo = {
        "A": [(vecino, costo), ...],
        ...
    }

Cada nodo se identifica con una letra (A, B, ... Z, AA, AB, ...) asignada en
el orden de recorrido del laberinto original.

Referencia del laberinto original:
    # 0 = libre, 1 = pared, 9 = meta, 2 = premio, 3 = penalización
    # Costos: 0 = 4,  2 = 1,  3 = 12
    laberinto = [
        [0, 0, 0, 0, 3, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0],
        [1, 1, 2, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 2, 0, 1, 3, 9, 2],
        [0, 1, 1, 1, 3, 2, 2, 1, 2],
        [0, 0, 1, 0, 0, 1, 2, 2, 2],
    ]

networkx y matplotlib se usan ÚNICAMENTE para dibujar el grafo.
"""

import networkx as nx
import matplotlib.pyplot as plt


INICIO = "A"
META = "AO"

# ---------------------------------------------------------------------------
# LISTA DE ADYACENCIA — cada arista con su costo (MODIFICA LOS COSTOS AQUÍ)
# Cada nodo es una letra: A, B, ... Z, AA, AB, ...
# ---------------------------------------------------------------------------
grafo = {
    "A": [("I", 4), ("B", 4)],
    "B": [("A", 4), ("C", 4)],
    "C": [("B", 4), ("D", 4)],
    "D": [("C", 4), ("E", 12)],
    "E": [("J", 4), ("D", 4), ("F", 4)],
    "F": [("E", 12), ("G", 4)],
    "G": [("K", 4), ("F", 4)],
    "H": [("L", 4)],
    "I": [("A", 4), ("M", 4)],
    "J": [("E", 12), ("P", 4)],
    "K": [("G", 4), ("Q", 4)],
    "L": [("H", 4), ("S", 4)],
    "M": [("I", 4), ("N", 4)],
    "N": [("M", 4), ("O", 4)],
    "O": [("T", 1), ("N", 4)],
    "P": [("J", 4), ("V", 4)],
    "Q": [("K", 4), ("R", 4)],
    "R": [("Q", 4), ("S", 4)],
    "S": [("L", 4), ("W", 4), ("R", 4)],
    "T": [("O", 4), ("Z", 4), ("U", 4)],
    "U": [("T", 1), ("V", 4)],
    "V": [("P", 4), ("AA", 4), ("U", 4)],
    "W": [("S", 4), ("AD", 4)],
    "X": [("AE", 4), ("Y", 4)],
    "Y": [("X", 4), ("Z", 4)],
    "Z": [("T", 1), ("AF", 4), ("Y", 4)],
    "AA": [("V", 4), ("AG", 4), ("AB", 12)],
    "AB": [("AA", 12), ("AC", 4)],
    "AC": [("AH", 4), ("AB", 4)],
    "AD": [("W", 4), ("AI", 4)],
    "AE": [("X", 4), ("AJ", 4)],
    "AF": [("Z", 4), ("AK", 4)],
    "AG": [("AA", 4), ("AM", 4)],
    "AH": [("AC", 4), ("AN", 12)],
    "AI": [("AD", 4), ("AP", 1)],
    "AJ": [("AE", 4), ("AQ", 4)],
    "AK": [("AF", 4), ("AL", 1)],
    "AL": [("AK", 4), ("AM", 4)],
    "AM": [("AG", 4), ("AR", 12), ("AL", 1)],
    "AN": [("AH", 4), ("AT", 1), ("AO", 4)],
    "AO": [("AN", 12), ("AP", 1)],
    "AP": [("AI", 4), ("AU", 1), ("AO", 4)],
    "AQ": [("AJ", 4), ("AV", 4)],
    "AR": [("AM", 4), ("AY", 4), ("AS", 1)],
    "AS": [("AR", 1), ("AT", 1)],
    "AT": [("AN", 1), ("AZ", 1), ("AS", 1)],
    "AU": [("AP", 1), ("BB", 1)],
    "AV": [("AQ", 4), ("AW", 4)],
    "AW": [("AV", 4)],
    "AX": [("AY", 4)],
    "AY": [("AR", 12), ("AX", 4)],
    "AZ": [("AT", 1), ("BA", 1)],
    "BA": [("AZ", 1), ("BB", 1)],
    "BB": [("AU", 1), ("BA", 1)],
}

# Posición de cada nodo para dibujar (columna como X, -fila como Y en el
# laberinto original). Define una disposición ordenada en el plano.
POSICIONES = {
    "A": (0, 0), "B": (1, 0), "C": (2, 0), "D": (3, 0), "E": (4, 0),
    "F": (5, 0), "G": (6, 0), "H": (8, 0),
    "I": (0, -1), "J": (4, -1), "K": (6, -1), "L": (8, -1),
    "M": (0, -2), "N": (1, -2), "O": (2, -2), "P": (4, -2),
    "Q": (6, -2), "R": (7, -2), "S": (8, -2),
    "T": (2, -3), "U": (3, -3), "V": (4, -3), "W": (8, -3),
    "X": (0, -4), "Y": (1, -4), "Z": (2, -4), "AA": (4, -4),
    "AB": (5, -4), "AC": (6, -4), "AD": (8, -4),
    "AE": (0, -5), "AF": (2, -5), "AG": (4, -5), "AH": (6, -5), "AI": (8, -5),
    "AJ": (0, -6), "AK": (2, -6), "AL": (3, -6), "AM": (4, -6),
    "AN": (6, -6), "AO": (7, -6), "AP": (8, -6),
    "AQ": (0, -7), "AR": (4, -7), "AS": (5, -7), "AT": (6, -7), "AU": (8, -7),
    "AV": (0, -8), "AW": (1, -8), "AX": (3, -8), "AY": (4, -8),
    "AZ": (6, -8), "BA": (7, -8), "BB": (8, -8),
}


# ---------------------------------------------------------------------------
# ALGORITMOS DE BÚSQUEDA (trabajan directamente sobre la lista de adyacencia)
# ---------------------------------------------------------------------------

def bfs(grafo, inicio, objetivo):
    """
    Búsqueda en Anchura. Cola FIFO (pop(0)).
    Explora nivel por nivel: garantiza el camino con menos pasos.
    Ignora los costos.
    """
    cola = [inicio]
    visitados = {inicio}
    predecesor = {inicio: None}
    orden_visita = [inicio]

    while cola:
        nodo = cola.pop(0)

        if nodo == objetivo:
            return reconstruir_camino(predecesor, objetivo), orden_visita

        for vecino, _peso in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                cola.append(vecino)
                orden_visita.append(vecino)

    return None, orden_visita


def dfs(grafo, inicio, objetivo):
    """
    Búsqueda en Profundidad. Pila LIFO (pop(-1)).
    Explora rama a rama: no garantiza el camino más corto.
    Ignora los costos.
    """
    pila = [inicio]
    visitados = {inicio}
    predecesor = {inicio: None}
    orden_visita = [inicio]

    while pila:
        nodo = pila.pop(-1)

        if nodo == objetivo:
            return reconstruir_camino(predecesor, objetivo), orden_visita

        for vecino, _peso in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                pila.append(vecino)
                orden_visita.append(vecino)

    return None, orden_visita


def ucs(grafo, inicio, objetivo):
    """
    Búsqueda de Costo Uniforme. Expande siempre el nodo de menor costo
    acumulado usando el peso de cada arista.
    Garantiza el camino de MENOR COSTO total.
    """
    dist = {inicio: 0}
    predecesor = {inicio: None}
    frontera = [(0, inicio)]       # (costo acumulado, nodo)
    orden_visita = []

    while frontera:
        frontera.sort(key=lambda x: x[0])   # menor costo primero
        costo, nodo = frontera.pop(0)

        if costo > dist.get(nodo, float("inf")):
            continue  # entrada obsoleta

        orden_visita.append(nodo)

        if nodo == objetivo:
            return reconstruir_camino(predecesor, objetivo), orden_visita

        for vecino, peso in grafo.get(nodo, []):
            nuevo_costo = costo + peso
            if nuevo_costo < dist.get(vecino, float("inf")):
                dist[vecino] = nuevo_costo
                predecesor[vecino] = nodo
                frontera.append((nuevo_costo, vecino))

    return None, orden_visita


def reconstruir_camino(predecesor, objetivo):
    """Reconstruye la ruta desde el inicio hasta el objetivo usando predecesores."""
    camino = []
    actual = objetivo
    while actual is not None:
        camino.append(actual)
        actual = predecesor[actual]
    return list(reversed(camino))


def costo_arista(grafo, u, v):
    """Devuelve el costo de la arista u-v (según cómo esté definida en 'grafo')."""
    for vecino, peso in grafo.get(u, []):
        if vecino == v:
            return peso
    return 0


def costo_total(grafo, camino):
    """Suma los costos de las aristas que componen la ruta."""
    if not camino or len(camino) < 2:
        return 0
    return sum(costo_arista(grafo, camino[i], camino[i + 1])
               for i in range(len(camino) - 1))


# ---------------------------------------------------------------------------
# VISUALIZACIÓN (networkx solo para dibujar)
# ---------------------------------------------------------------------------

def construir_grafo_nx():
    """Convierte la lista de adyacencia en un grafo de networkx para graficar."""
    G = nx.Graph()
    for nodo, vecinos in grafo.items():
        G.add_node(nodo)
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)
    return G


def dibujar(G, titulo, subtitulos, aviso, colores_nodo, camino=None):
    """Dibuja el grafo con colores de nodo dados y resalta la ruta si se pasa."""
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

    pesos = nx.get_edge_attributes(G, "weight")

    fig = plt.figure(figsize=(9, 9))
    nx.draw(
        G,
        pos=POSICIONES,
        with_labels=True,
        labels={n: n for n in G.nodes()},
        node_color=colores_nodo,
        edge_color=aristas_color,
        width=aristas_ancho,
        node_size=500,
        font_size=6,
    )
    nx.draw_networkx_edge_labels(G, POSICIONES, edge_labels=pesos, font_size=6)

    fig.text(0.5, 0.97, titulo, ha="center", va="top",
             fontsize=10, fontweight="bold")
    y = 0.93
    for st in subtitulos:
        fig.text(0.5, y, st, ha="center", va="top", fontsize=8)
        y -= 0.03
    fig.text(0.5, 0.01, aviso, ha="center", va="bottom", fontsize=9,
             color="white",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="steelblue", edgecolor="none"))
    plt.show()


def dibujar_inicial(G):
    colores = []
    for nodo in G.nodes():
        if nodo == INICIO:
            colores.append("orange")
        elif nodo == META:
            colores.append("green")
        else:
            colores.append("lightgray")
    dibujar(
        G,
        "Laberinto (lista de adyacencia) — Estado inicial",
        ["Naranja: inicio  |  Verde: meta",
         "Los números sobre las aristas son el costo (peso)"],
        "Cierra esta ventana para elegir el algoritmo",
        colores,
    )


def dibujar_resultado(G, algoritmo, camino, visitados):
    conjunto_ruta = set(camino) if camino else set()
    colores = []
    for nodo in G.nodes():
        if nodo in conjunto_ruta:
            if nodo == INICIO:
                colores.append("orange")
            elif nodo == META:
                colores.append("red")
            else:
                colores.append("limegreen")
        elif nodo in visitados:
            colores.append("steelblue")
        else:
            colores.append("lightgray")

    pasos = len(camino) - 1 if camino else 0
    titulo = (f"Algoritmo: {algoritmo}  |  Explorados: {len(visitados)}  |  "
              f"Pasos: {pasos}  |  Costo total: {costo_total(grafo, camino)}")
    if not camino:
        titulo += "  |  No se encontró camino"

    dibujar(G, titulo, [], "Cierra esta ventana para continuar", colores, camino)


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    print("=" * 50)
    print("   LABERINTO (LISTA DE ADYACENCIA) — BÚSQUEDA")
    print("=" * 50)
    print(f"  Inicio : {INICIO}")
    print(f"  Meta   : {META}")
    print(f"  Nodos  : {len(grafo)}")
    print("=" * 50)

    G = construir_grafo_nx()

    print("\nMostrando el laberinto inicial...")
    dibujar_inicial(G)

    print("\n¿Con qué algoritmo deseas resolverlo?")
    print("  (1) BFS — Búsqueda en Anchura (menos pasos)")
    print("  (2) DFS — Búsqueda en Profundidad")
    print("  (3) UCS — Búsqueda de Costo Uniforme (menor costo)")
    print("  (0) Salir del programa")

    while True:
        opcion = input("\nIngresa 1, 2 o 3: ").strip()
        if opcion in ("1", "2", "3"):
            break
        if opcion == "0":
            return
        print("  Opción no válida, ingresa 1, 2 o 3.")

    if opcion == "1":
        nombre, (camino, visitados) = "BFS", bfs(grafo, INICIO, META)
    elif opcion == "2":
        nombre, (camino, visitados) = "DFS", dfs(grafo, INICIO, META)
    else:
        nombre, (camino, visitados) = "UCS", ucs(grafo, INICIO, META)

    print(f"\n--- Resultado {nombre} ---")
    if camino:
        print(f"  Ruta encontrada ({len(camino) - 1} pasos):")
        print(f"  {' → '.join(str(n) for n in camino)}")
        print(f"  Costo total de la ruta: {costo_total(grafo, camino)}")
    else:
        print("  No se encontró un camino hacia la meta.")
    print(f"  Nodos explorados: {len(visitados)}")
    print(f"  Orden de exploración: {visitados}")

    print("\nMostrando resultado visual...")
    print("  Azul = explorados  |  Verde = ruta  |  Naranja = inicio  |  Rojo = meta")
    dibujar_resultado(G, nombre, camino, set(visitados))


if __name__ == "__main__":
    main()
