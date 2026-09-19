# Laberinto con NetworkX

Programa en Python que representa un laberinto como un **grafo** utilizando la librería [NetworkX](https://networkx.org/), y permite recorrerlo manualmente controlando a un jugador desde el teclado.

## Descripción

La matriz del laberinto se transforma automáticamente en un grafo (`nx.Graph()`), donde:

- Cada celda que **no** es un muro se convierte en un **nodo**, identificado por su coordenada `(fila, columna)`.
- Se crea una **arista** entre dos nodos si sus celdas son adyacentes (arriba, abajo, izquierda o derecha). No se permiten movimientos en diagonal.

El jugador se mueve por el grafo introduciendo comandos por teclado. **No se utiliza ningún algoritmo de búsqueda de caminos** (nada de BFS, DFS, A* ni `shortest_path()`): el propio usuario decide hacia dónde moverse en cada turno, y el programa solo comprueba con NetworkX (`G.has_edge()`) si ese movimiento es válido.

## Valores del laberinto

| Valor | Significado    |
|-------|-----------------|
| `0`   | Camino libre    |
| `1`   | Muro (no transitable, no genera nodo) |
| `2`   | Penalización (-5 monedas) |
| `3`   | Premio (+10 monedas) |
| `9`   | Meta            |

## Requisitos

- Python 3.8+
- [NetworkX](https://networkx.org/)
- [Matplotlib](https://matplotlib.org/) (para dibujar el grafo)

Instalación de dependencias:

```bash
pip install networkx matplotlib
```

## Cómo ejecutarlo

```bash
python laberinto.py
```

Al iniciar, se abrirá una ventana con el dibujo del grafo del laberinto completo. Ciérrala para continuar y comenzar a jugar desde la consola.

## Controles

| Tecla | Movimiento |
|-------|------------|
| `w`   | Arriba     |
| `s`   | Abajo      |
| `a`   | Izquierda  |
| `d`   | Derecha    |
| `ver` | Vuelve a dibujar el grafo con la posición actual |
| `salir` | Termina la partida |

Ejemplo de turno:

```
Movimiento: d
```

El programa calcula la celda destino según la dirección elegida y comprueba con `G.has_edge(pos, destino)` si existe una conexión (camino libre) entre la posición actual y esa celda. Si existe, el jugador se mueve; si no, se le informa de que hay un muro.

## Reglas del juego

- El jugador comienza en la posición `(0, 0)` con `30` monedas.
- Pisar una celda de **penalización** (`2`) resta 5 monedas.
- Pisar una celda de **premio** (`3`) suma 10 monedas.
- Llegar a la celda de **meta** (`9`) termina la partida con victoria.
- Si las monedas llegan a `0` o menos, la partida termina.

## Visualización del grafo

El grafo se dibuja con `matplotlib`, usando la propia coordenada `(fila, columna)` de cada celda como su posición en el plano. Los colores indican:

- 🔵 Azul: posición actual del jugador
- ⚪ Gris claro: camino libre
- 🟠 Naranja: penalización
- 🟡 Dorado: premio
- 🟢 Verde: meta

El dibujo se actualiza automáticamente tras cada movimiento válido, y también puede volver a mostrarse en cualquier momento escribiendo `ver`.
