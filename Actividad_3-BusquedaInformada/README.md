# Actividad 3 – Búsqueda informada con A*

Solución de un laberinto de 10×10 con el algoritmo A* usando tres heurísticas: Manhattan, Euclidiana y Chebyshev. El programa compara cuántos nodos expande cada una y muestra el camino encontrado.

## Integrantes

- Michael Stevens Cardenas Urbano (2610304)
- Luis Santiago Arenas Hincapié (2435300)
- Brigitte Vanesa Chavez Riascos (2510107)

## Descripción

El laberinto es una matriz donde:

| Valor | Significado |
|-------|-------------|
| 0 | Casilla transitable |
| 1 | Pared |
| 2 | Inicio |
| 3 | Meta |

Los movimientos son arriba, abajo, izquierda y derecha, y cada paso cuesta 1. A* expande el nodo con menor `f(n) = g(n) + h(n)`, y los empates se resuelven por menor `g`.

## Heurísticas

| Heurística | Fórmula | Admisible | Monótona |
|------------|---------|-----------|----------|
| H1: Manhattan | \|Δfila\| + \|Δcol\| | Sí | Sí |
| H2: Euclidiana | √(Δfila² + Δcol²) | Sí | Sí |
| H3: Chebyshev | max(\|Δfila\|, \|Δcol\|) | Sí | Sí |

Se cumple `h3 ≤ h2 ≤ h1 ≤ h*`, donde `h*` es el costo real. Las demostraciones están en el informe.

## Resultados

| Heurística | h(inicio) | Nodos expandidos | Pasos |
|------------|-----------|------------------|-------|
| H1: Manhattan | 18,00 | 49 | 20 |
| H2: Euclidiana | 12,73 | 55 | 20 |
| H3: Chebyshev | 9,00 | 63 | 20 |

Las tres encuentran el camino óptimo de 20 pasos. Manhattan es la más dominante (menos exploración) y Chebyshev la menos efectiva.

## Requisitos

- Python 3.8 o superior
- matplotlib

```bash
pip install matplotlib
```

## Ejecución

```bash
python laberinto_informado.py
```

El programa muestra primero el laberinto sin resolver y después un gráfico por cada heurística, con el camino (amarillo) y los nodos explorados (azul claro). Se debe cerrar cada ventana para ver la siguiente. En la terminal se imprime la tabla comparativa y el análisis de dominancia.

## Estructura

```
.
├── laberinto_informado.py   # Código: A*, heurísticas y visualización
├── informe.tex              # Informe en LaTeX (Overleaf)
├── figuras/                 # Imágenes usadas en el informe
└── README.md
```
