import networkx as nx
import matplotlib.pyplot as plt

# 0 = camino libre, 1 = pared, 9 = meta, 2 = Premio, 3 = Penalización
# Costos (Weight): 0 = 4unid , 2 = 1unid , 3 = 12unid
laberinto = [
    [0, 0, 0, 0, 3, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 2, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 2, 0, 1, 3, 9, 2],
    [0, 1, 1, 1, 3, 2, 2, 1, 2],
    [0, 0, 1, 0, 0, 1, 2, 2, 2]
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

# Costo (peso) asociado al TIPO de celda a la que se entra.
# El costo de una arista = costo de la celda destino.
COSTOS_CELDA = {
    0: 4,   # camino libre
    2: 1,   # premio
    3: 12,  # penalización
}
COSTO_META = 4  # la meta (9) es transitable; se le asigna el costo de celda libre


def costo_celda(valor):
    """Devuelve el costo de entrar a una celda según su valor."""
    if valor == 9:
        return COSTO_META
    return COSTOS_CELDA.get(valor, 4)


# --- Construcción automática del grafo a partir de la matriz ---
G = nx.Graph()

# Crear un nodo por cada celda que no sea muro (1)
for f in range(filas):
    for c in range(columnas):
        if laberinto[f][c] != 1:
            G.add_node((f, c), valor=laberinto[f][c])

# Crear aristas entre celdas adyacentes (arriba/abajo/izq/der) que no sean muro.
# El peso de la arista se calcula a partir del valor de la celda destino.
for f in range(filas):
    for c in range(columnas):
        if laberinto[f][c] == 1:
            continue

        actual = (f, c)

        # Vecino de abajo
        if f + 1 < filas and laberinto[f + 1][c] != 1:
            destino = (f + 1, c)
            G.add_edge(actual, destino, weight=costo_celda(laberinto[f + 1][c]))

        # Vecino de la derecha
        if c + 1 < columnas and laberinto[f][c + 1] != 1:
            destino = (f, c + 1)
            G.add_edge(actual, destino, weight=costo_celda(laberinto[f][c + 1]))


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


def ucs(grafo, inicio, objetivo):
    """
    Búsqueda de Costo Uniforme (UCS / Uniform Cost Search).
    Expande siempre el nodo con menor costo acumulado desde el inicio,
    usando el peso (weight) de cada arista.
    Garantiza el camino de MENOR COSTO total (no de menos pasos).
    """
    dist = {inicio: 0}             # mejor costo conocido hasta cada nodo
    predecesor = {inicio: None}    # para reconstruir el camino
    frontera = [(0, inicio)]       # lista de (costo acumulado, nodo)
    orden_visita = []              # registro del orden de expansión

    while frontera:
        # Seleccionar el nodo con menor costo acumulado (cola de prioridad simple)
        frontera.sort(key=lambda x: x[0])
        costo, nodo = frontera.pop(0)

        # Ignorar entradas obsoletas (ya encontramos un camino mejor a ese nodo)
        if costo > dist.get(nodo, float("inf")):
            continue

        orden_visita.append(nodo)

        if nodo == objetivo:
            # Reconstrucción del camino desde meta hasta inicio
            camino = []
            actual = objetivo
            while actual is not None:
                camino.append(actual)
                actual = predecesor[actual]
            return list(reversed(camino)), orden_visita

        # Expandir vecinos usando el peso de la arista
        for vecino in grafo.neighbors(nodo):
            peso = grafo[nodo][vecino]["weight"]
            nuevo_costo = costo + peso
            if nuevo_costo < dist.get(vecino, float("inf")):
                dist[vecino] = nuevo_costo
                predecesor[vecino] = nodo
                frontera.append((nuevo_costo, vecino))

    return None, orden_visita  # no se encontró camino


def costo_total(camino):
    """Suma los pesos de las aristas que componen una ruta."""
    if not camino or len(camino) < 2:
        return 0
    return sum(
        G[camino[i]][camino[i + 1]]["weight"]
        for i in range(len(camino) - 1)
    )


# ---------------------------------------------------------------------------
# VISUALIZACIÓN
# ---------------------------------------------------------------------------

POS_GRAFO = {nodo: (nodo[1], -nodo[0]) for nodo in G.nodes()}


def color_por_tipo(nodo):
    """Devuelve el color base de un nodo según el tipo de celda."""
    valor = laberinto[nodo[0]][nodo[1]]
    if valor == 9:
        return "green"        # meta
    elif valor == 2:
        return "gold"         # premio
    elif valor == 3:
        return "indianred"    # penalización
    return "lightgray"        # camino libre


def dibujar_laberinto_inicial():
    """Muestra el grafo del laberinto sin ningún recorrido aplicado."""
    colores = []
    for nodo in G.nodes():
        if nodo == INICIO:
            colores.append("orange")          # inicio
        else:
            colores.append(color_por_tipo(nodo))

    # Pesos de las aristas para mostrarlos como etiquetas
    pesos = nx.get_edge_attributes(G, "weight")

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
    nx.draw_networkx_edge_labels(G, POS_GRAFO, edge_labels=pesos, font_size=6)

    fig.text(0.5, 0.97, "Laberinto — Estado inicial",
             ha="center", va="top", fontsize=11, fontweight="bold")
    fig.text(0.5, 0.93,
             "Naranja: inicio  |  Verde: meta  |  Dorado: premio  |  Rojo: penalización",
             ha="center", va="top", fontsize=8)
    fig.text(0.5, 0.90,
             "Los números sobre las aristas son el costo (peso)",
             ha="center", va="top", fontsize=8, style="italic")
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
    costo_ruta = costo_total(camino)
    titulo = (
        f"Algoritmo: {algoritmo}  |  "
        f"Nodos explorados: {len(visitados)}  |  "
        f"Pasos: {pasos_ruta}  |  "
        f"Costo total: {costo_ruta}"
    )
    if not camino:
        titulo += "  |  ⚠ No se encontró camino"

    pesos = nx.get_edge_attributes(G, "weight")

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
    nx.draw_networkx_edge_labels(G, POS_GRAFO, edge_labels=pesos, font_size=6)

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
        nombre = "BFS"
        camino, visitados = bfs(G, INICIO, META)
    elif opcion == "2":
        nombre = "DFS"
        camino, visitados = dfs(G, INICIO, META)
    else:
        nombre = "UCS"
        camino, visitados = ucs(G, INICIO, META)

    # Mostrar resultados en consola
    print(f"\n--- Resultado {nombre} ---")
    if camino:
        print(f"  Ruta encontrada ({len(camino) - 1} pasos):")
        print(f"  {' → '.join(str(n) for n in camino)}")
        print(f"  Costo total de la ruta: {costo_total(camino)}")
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
