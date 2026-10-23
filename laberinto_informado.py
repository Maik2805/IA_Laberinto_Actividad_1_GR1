"""Laberinto 10×10 resuelto con A* usando tres heurísticas.

Valores de la matriz:
    0 = casilla transitable
    1 = pared
    2 = inicio
    3 = meta

El algoritmo A* combina:
    f(n) = g(n) + h(n)
donde g(n) es el costo real desde el inicio y h(n) es la estimación heurística.

Heurísticas implementadas:
    H1: Manhattan  — |Δx| + |Δy|
    H2: Euclidiana — √(Δx² + Δy²)
    H3: Chebyshev  — max(|Δx|, |Δy|)

Requisito: matplotlib (pip install matplotlib)
"""

import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

# ---------------------------------------------------------------------------
# LABERINTO 10×10
# 0 = transitable, 1 = pared, 2 = inicio, 3 = meta
# ---------------------------------------------------------------------------
LABERINTO = [
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 3],
]

COSTO_MOVIMIENTO = 1  # Costo uniforme para cada paso

VALOR_A_SIMBOLO = {0: ".", 1: "#", 2: "S", 3: "G"}


# ---------------------------------------------------------------------------
# HEURÍSTICAS
# ---------------------------------------------------------------------------

def h_manhattan(nodo, objetivo):
    """H1: Distancia Manhattan — suma de diferencias absolutas en X e Y.
    
    Admisible: Sí. Nunca sobreestima porque asume el camino ideal sin obstáculos,
               y con costo 1 por paso, la distancia real siempre es ≥ Manhattan.
    Monótona: Sí. Para un paso de costo 1: h(n) ≤ 1 + h(n') porque al moverse
              una casilla, la distancia Manhattan cambia como máximo en 1.
    """
    return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])


def h_euclidiana(nodo, objetivo):
    """H2: Distancia Euclidiana — línea recta entre dos puntos.
    
    Admisible: Sí. Es la distancia más corta posible (línea recta),
               por lo tanto nunca puede sobreestimar el costo real.
    Monótona: Sí. La distancia euclidiana cumple la desigualdad triangular.
    """
    return math.sqrt((nodo[0] - objetivo[0])**2 + (nodo[1] - objetivo[1])**2)


def h_chebyshev(nodo, objetivo):
    """H3: Distancia Chebyshev — máximo de las diferencias absolutas.
    
    Admisible: Sí. Representa el mínimo de pasos si se permitieran diagonales.
               Como aquí solo hay movimientos ortogonales, el costo real es ≥ Chebyshev.
    Monótona: Sí. Al moverse una casilla ortogonalmente, Chebyshev cambia como máximo en 1.
    """
    return max(abs(nodo[0] - objetivo[0]), abs(nodo[1] - objetivo[1]))


HEURISTICAS = {
    "H1: Manhattan": h_manhattan,
    "H2: Euclidiana": h_euclidiana,
    "H3: Chebyshev": h_chebyshev,
}


# ---------------------------------------------------------------------------
# UTILIDADES DEL LABERINTO
# ---------------------------------------------------------------------------

def encontrar_posicion(matriz, valor):
    """Encuentra la posición (fila, columna) de un valor en la matriz."""
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            if matriz[fila][col] == valor:
                return (fila, col)
    return None


def obtener_vecinos(matriz, nodo):
    """Devuelve los vecinos transitables (arriba, abajo, izquierda, derecha)."""
    fila, col = nodo
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izq, der
    
    for df, dc in movimientos:
        nueva_fila, nueva_col = fila + df, col + dc
        if 0 <= nueva_fila < len(matriz) and 0 <= nueva_col < len(matriz[0]):
            if matriz[nueva_fila][nueva_col] != 1:  # no es pared
                vecinos.append((nueva_fila, nueva_col))
    return vecinos


# ---------------------------------------------------------------------------
# ALGORITMO A*
# ---------------------------------------------------------------------------

def a_estrella(matriz, inicio, objetivo, heuristica):
    """
    Algoritmo A*: expande nodos por f(n) = g(n) + h(n).
    
    Retorna: (camino, nodos_explorados, orden_visita)
    - camino: lista de posiciones desde inicio hasta meta, o None si no hay solución
    - nodos_explorados: cantidad de nodos expandidos
    - orden_visita: lista con el orden en que se expandieron los nodos
    """
    g = {inicio: 0}  # costo real desde inicio
    predecesor = {inicio: None}
    # frontera: (f, g, nodo) — ordenamos por f, desempatamos por g
    frontera = [(heuristica(inicio, objetivo), 0, inicio)]
    orden_visita = []
    
    while frontera:
        # Ordenar por f (menor primero), desempatar por g (menor primero)
        frontera.sort(key=lambda x: (x[0], x[1]))
        f, costo, nodo = frontera.pop(0)
        
        # Saltar entradas obsoletas
        if costo > g.get(nodo, float("inf")):
            continue
        
        orden_visita.append(nodo)
        
        # ¿Llegamos a la meta?
        if nodo == objetivo:
            camino = reconstruir_camino(predecesor, objetivo)
            return camino, len(orden_visita), orden_visita
        
        # Expandir vecinos
        for vecino in obtener_vecinos(matriz, nodo):
            nuevo_g = costo + COSTO_MOVIMIENTO
            if nuevo_g < g.get(vecino, float("inf")):
                g[vecino] = nuevo_g
                nuevo_f = nuevo_g + heuristica(vecino, objetivo)
                predecesor[vecino] = nodo
                frontera.append((nuevo_f, nuevo_g, vecino))
    
    return None, len(orden_visita), orden_visita


def reconstruir_camino(predecesor, objetivo):
    """Reconstruye el camino desde el inicio hasta el objetivo."""
    camino = []
    actual = objetivo
    while actual is not None:
        camino.append(actual)
        actual = predecesor[actual]
    return list(reversed(camino))


# ---------------------------------------------------------------------------
# VALIDACIÓN
# ---------------------------------------------------------------------------

def validar_laberinto(matriz):
    """Valida que el laberinto tenga la estructura correcta."""
    if len(matriz) != 10 or any(len(fila) != 10 for fila in matriz):
        raise ValueError("El laberinto debe tener exactamente 10 filas de 10 columnas.")

    valores_validos = {0, 1, 2, 3}
    for num_fila, fila in enumerate(matriz):
        invalidos = set(fila) - valores_validos
        if invalidos:
            raise ValueError(f"Valores no válidos en la fila {num_fila}: {invalidos}")

    total_inicio = sum(fila.count(2) for fila in matriz)
    total_meta = sum(fila.count(3) for fila in matriz)

    if total_inicio != 1:
        raise ValueError("El laberinto debe contener exactamente un inicio (2).")
    if total_meta != 1:
        raise ValueError("El laberinto debe contener exactamente una meta (3).")


def imprimir_laberinto(matriz):
    """Imprime el laberinto en la terminal con símbolos legibles."""
    print("Laberinto 10 × 10")
    print("S = inicio | G = meta | # = pared | . = transitable\n")
    print("    " + " ".join(str(c) for c in range(10)))
    for num_fila, fila in enumerate(matriz):
        simbolos = " ".join(VALOR_A_SIMBOLO[v] for v in fila)
        print(f"{num_fila:>2}  {simbolos}")


# ---------------------------------------------------------------------------
# VISUALIZACIÓN
# ---------------------------------------------------------------------------

def visualizar_laberinto(matriz, titulo="Laberinto 10 × 10", camino=None, explorados=None):
    """Dibuja la matriz como una cuadrícula con colores, ruta y nodos explorados."""
    # Crear copia para no modificar la original
    matriz_visual = [fila[:] for fila in matriz]
    
    colores = [
        "#F1F5F9",  # 0: transitable
        "#374151",  # 1: pared
        "#22C55E",  # 2: inicio
        "#3B82F6",  # 3: meta
        "#93C5FD",  # 4: explorado (azul claro)
        "#FDE047",  # 5: camino (amarillo)
    ]
    mapa_colores = ListedColormap(colores)
    limites_colores = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5], mapa_colores.N)
    
    # Marcar nodos explorados
    if explorados:
        for (fila, col) in explorados:
            if matriz_visual[fila][col] == 0:
                matriz_visual[fila][col] = 4
    
    # Marcar camino
    if camino:
        for (fila, col) in camino:
            if matriz_visual[fila][col] in (0, 4):
                matriz_visual[fila][col] = 5

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(matriz_visual, cmap=mapa_colores, norm=limites_colores, interpolation="none")

    # Mostrar S y G dentro de sus casillas
    inicio = encontrar_posicion(matriz, 2)
    meta = encontrar_posicion(matriz, 3)
    
    if inicio:
        ax.text(inicio[1], inicio[0], "S", ha="center", va="center",
                fontsize=15, fontweight="bold", color="#064E3B")
    if meta:
        ax.text(meta[1], meta[0], "G", ha="center", va="center",
                fontsize=15, fontweight="bold", color="white")

    # Cuadrícula que separa las casillas
    ax.set_xticks([i - 0.5 for i in range(11)], minor=True)
    ax.set_yticks([i - 0.5 for i in range(11)], minor=True)
    ax.grid(which="minor", color="white", linewidth=1.8)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Coordenadas
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.set_xticklabels(range(10))
    ax.set_yticklabels(range(10))
    ax.set_xlabel("Columna", fontsize=11, labelpad=8)
    ax.set_ylabel("Fila", fontsize=11, labelpad=8)
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=14)

    leyenda = [
        Patch(facecolor=colores[0], edgecolor="#CBD5E1", label="Transitable"),
        Patch(facecolor=colores[1], label="Pared"),
        Patch(facecolor=colores[2], label="Inicio (S)"),
        Patch(facecolor=colores[3], label="Meta (G)"),
    ]
    if explorados:
        leyenda.append(Patch(facecolor=colores[4], label="Explorado"))
    if camino:
        leyenda.append(Patch(facecolor=colores[5], label="Camino"))
    
    ax.legend(handles=leyenda, loc="upper center", bbox_to_anchor=(0.5, -0.09),
              ncol=len(leyenda), frameon=False)

    fig.tight_layout()
    return fig, ax


def visualizar_resultado_heuristica(matriz, nombre_h, camino, explorados, nodos_expandidos):
    """Visualiza el resultado de A* con una heurística específica."""
    inicio = encontrar_posicion(matriz, 2)
    meta = encontrar_posicion(matriz, 3)
    
    # Obtener la función heurística
    h_func = HEURISTICAS[nombre_h]
    
    # Calcular h(inicio) para mostrar
    h_inicio = h_func(inicio, meta)
    
    # Información de la heurística
    info_heuristicas = {
        "H1: Manhattan": {
            "formula": "|Δfila| + |Δcol|",
            "admisible": "Sí (nunca sobreestima: asume camino sin obstáculos)",
            "monotona": "Sí (h(n) ≤ 1 + h(n') para pasos de costo 1)",
        },
        "H2: Euclidiana": {
            "formula": "√(Δfila² + Δcol²)",
            "admisible": "Sí (línea recta = distancia mínima posible)",
            "monotona": "Sí (cumple desigualdad triangular)",
        },
        "H3: Chebyshev": {
            "formula": "max(|Δfila|, |Δcol|)",
            "admisible": "Sí (mínimo con diagonales ≤ costo real ortogonal)",
            "monotona": "Sí (cambia máximo 1 por paso ortogonal)",
        },
    }
    
    info = info_heuristicas[nombre_h]
    pasos = len(camino) - 1 if camino else 0
    
    titulo = f"A* con {nombre_h}"
    fig, ax = visualizar_laberinto(matriz, titulo, camino, explorados)
    
    # Añadir información debajo del gráfico
    texto_info = (
        f"Fórmula: {info['formula']}  |  h(inicio) = {h_inicio:.2f}\n"
        f"Admisible: {info['admisible']}\n"
        f"Monótona: {info['monotona']}\n"
        f"Nodos explorados: {nodos_expandidos}  |  Pasos hasta meta: {pasos}"
    )
    
    fig.text(0.5, 0.02, texto_info, ha="center", va="bottom", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#E0F2FE", edgecolor="#0284C7"))
    
    plt.subplots_adjust(bottom=0.22)
    return fig


def main():
    validar_laberinto(LABERINTO)
    imprimir_laberinto(LABERINTO)
    
    inicio = encontrar_posicion(LABERINTO, 2)
    meta = encontrar_posicion(LABERINTO, 3)
    
    print(f"\nInicio: {inicio} (fila, columna)")
    print(f"Meta:   {meta} (fila, columna)")
    print(f"Costo por movimiento: {COSTO_MOVIMIENTO}")
    
    # 1) Mostrar laberinto sin resolver
    print("\n" + "=" * 60)
    print("Mostrando laberinto sin resolver...")
    print("Cierra la ventana para continuar con la búsqueda A*")
    print("=" * 60)
    visualizar_laberinto(LABERINTO, "Laberinto 10 × 10 — Estado inicial")
    plt.show()
    
    # 2) Ejecutar A* con cada heurística y mostrar resultados
    print("\n" + "=" * 60)
    print("EJECUTANDO A* CON LAS TRES HEURÍSTICAS")
    print("=" * 60)
    
    resultados = {}
    
    for nombre_h, h_func in HEURISTICAS.items():
        print(f"\n--- {nombre_h} ---")
        camino, nodos_exp, orden = a_estrella(LABERINTO, inicio, meta, h_func)
        resultados[nombre_h] = {
            "camino": camino,
            "nodos_explorados": nodos_exp,
            "orden": orden,
            "pasos": len(camino) - 1 if camino else 0,
            "h_inicio": h_func(inicio, meta),
        }
        
        if camino:
            print(f"  Camino encontrado: {len(camino) - 1} pasos")
            print(f"  Nodos explorados: {nodos_exp}")
            print(f"  h(inicio) = {h_func(inicio, meta):.2f}")
        else:
            print("  No se encontró camino")
    
    # 3) Comparación de heurísticas
    print("\n" + "=" * 60)
    print("COMPARACIÓN DE HEURÍSTICAS")
    print("=" * 60)
    print(f"{'Heurística':<18} {'h(inicio)':<12} {'Explorados':<12} {'Pasos':<8}")
    print("-" * 50)
    
    for nombre_h, res in resultados.items():
        print(f"{nombre_h:<18} {res['h_inicio']:<12.2f} {res['nodos_explorados']:<12} {res['pasos']:<8}")
    
    # Determinar dominancia
    exploraciones = [(nombre, res["nodos_explorados"]) for nombre, res in resultados.items()]
    exploraciones.sort(key=lambda x: x[1])
    
    print("\n--- Análisis de Dominancia ---")
    print(f"  Más dominante (menos exploración): {exploraciones[0][0]} ({exploraciones[0][1]} nodos)")
    print(f"  Menos efectiva (más exploración):  {exploraciones[-1][0]} ({exploraciones[-1][1]} nodos)")
    
    print("\n" + "=" * 60)
    print("MOSTRANDO GRÁFICOS DE RESULTADOS")
    print("(Cierra cada ventana para ver la siguiente)")
    print("=" * 60)
    
    # 4) Mostrar un gráfico por cada heurística
    for nombre_h, res in resultados.items():
        print(f"\nMostrando resultado de {nombre_h}...")
        visualizar_resultado_heuristica(
            LABERINTO,
            nombre_h,
            res["camino"],
            res["orden"],
            res["nodos_explorados"]
        )
        plt.show()
    
    print("\n¡Análisis completado!")


if __name__ == "__main__":
    main()
