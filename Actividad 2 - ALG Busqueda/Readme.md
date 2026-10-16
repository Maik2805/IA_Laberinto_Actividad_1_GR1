# Laberinto con Algoritmos de Búsqueda

Programa que modela un laberinto como un grafo (lista de adyacencia) y lo resuelve automáticamente con **BFS**, **DFS** o **UCS**, según elija el usuario. Muestra la ruta encontrada y el proceso de exploración por consola y de forma visual.

#### **Readme construido con herramienta de IA.**
---

## Archivos

| Archivo | Descripción |
|---|---|
| `laberinto_BFS_DFS_UCS.py` | Define el laberinto como **lista de adyacencia** con costos explícitos y lo resuelve con BFS, DFS o UCS. |

---

## Requisitos

- Python 3.8 o superior
- Librerías `networkx` y `matplotlib`

Instalación de dependencias:

```bash
pip install networkx matplotlib
```

---

## Ejecución

```bash
python laberinto_BFS_DFS_UCS.py
```

Flujo del programa:

1. **Menú de algoritmo:** elegir BFS, DFS o UCS (o salir).
2. **Menú de costos** (solo BFS y DFS): elegir si se ejecuta **con costos** o **sin costos**.
3. **Resultado en consola:** ruta, pasos, nodos explorados y orden de exploración.
4. **Visualización:** se abre una ventana con el grafo y la ruta resaltada.

---

## Menús

### Menú de algoritmo

```
¿Con qué algoritmo deseas resolverlo?
  (1) BFS — Búsqueda en Anchura (menos pasos)
  (2) DFS — Búsqueda en Profundidad
  (3) UCS — Búsqueda de Costo Uniforme (menor costo)
  (0) Salir del programa
```

### Menú de costos (solo BFS y DFS)

```
¿Cómo deseas ejecutar el laberinto?
  (1) Con costos
  (2) Sin costos
```

| Modo | Qué se muestra |
|---|---|
| Con costos | Pesos sobre las aristas y **costo total** de la ruta (consola y título de la figura). |
| Sin costos | Solo la ruta, los pasos y los nodos explorados; se ocultan los pesos y el costo total. |

BFS y DFS no usan los costos para decidir el camino, así que la ruta encontrada es la misma en ambos modos; solo cambia la información mostrada. **UCS** no muestra este menú porque siempre trabaja con costos.

---

## Representación del grafo

El grafo se define como un diccionario donde cada nodo lista sus vecinos junto con el **costo explícito** de cada arista:

```python
grafo = {
    "A": [("I", 4), ("B", 4)],
    "B": [("A", 4), ("C", 4)],
    ...
}
```

- Los nodos se identifican con letras (`A`, `B`, ... `Z`, `AA`, `AB`, ...).
- **Inicio:** `A` — **Meta:** `AO`.
- Para cambiar un costo, basta modificar el número en la tupla correspondiente.

Los costos provienen del laberinto original en matriz:

| Valor | Significado | Costo |
|---|---|---|
| `0` | Camino libre | 4 |
| `1` | Pared (bloqueado) | — |
| `2` | Premio | 1 |
| `3` | Penalización | 12 |
| `9` | Meta | 4 |

Se usa lista de adyacencia para **definir los costos sin ambigüedad**: en un grafo no dirigido construido desde una matriz, el costo (propiedad de la celda) no se traslada de forma única a la arista. Aquí el costo se escribe directamente sobre cada conexión.

---

## Algoritmos de búsqueda

Los tres reciben el grafo, el inicio y la meta, y devuelven la **ruta encontrada** y el **orden de exploración**.

| Algoritmo | Estructura | Garantiza |
|---|---|---|
| BFS — Búsqueda en Anchura | Cola FIFO (`pop(0)`) | Ruta con **menos pasos**. Ignora costos. |
| DFS — Búsqueda en Profundidad | Pila LIFO (`pop(-1)`) | Nada: no asegura la ruta más corta ni la más barata. |
| UCS — Costo Uniforme | Cola de prioridad por costo acumulado | Ruta de **menor costo** total. |

Los tres comparten la misma mecánica: un contenedor de nodos pendientes, un registro de visitados y un diccionario `predecesor` para reconstruir el camino. La diferencia está en **cómo eligen el siguiente nodo**: cola, pila o prioridad por costo.

---

## Resultados en consola

Ejemplo con UCS:

```
--- Resultado UCS (con costos) ---
  Ruta encontrada (15 pasos):
  A → I → M → N → O → T → Z → AF → AK → AL → AM → AR → AS → AT → AN → AO
  Costo total de la ruta: 53
  Nodos explorados: 49
  Orden de exploración: ['A', 'I', 'B', ...]
```

---

## Visualización

Tras mostrar el resultado en consola se abre una ventana de matplotlib con el grafo:

| Color | Nodo |
|---|---|
| Azul | Explorado durante la búsqueda |
| Verde | Forma parte de la ruta encontrada |
| Naranja | Inicio |
| Rojo | Meta alcanzada |
| Gris claro | No visitado |

Las aristas de la ruta se pintan en verde con mayor grosor. En modo **con costos**, cada arista muestra su peso como etiqueta.

> Cierra la ventana para terminar el programa.

---

## Nota sobre el orden de exploración

En BFS y DFS, `orden_visita` registra el momento en que un nodo es **descubierto** (encolado o apilado), no cuando es explorado. Por eso la meta puede aparecer en la lista seguida de otros nodos: ya habían sido encolados antes de que el algoritmo extrajera y verificara la meta. En UCS se registra al **expandir** el nodo. La ruta devuelta es siempre correcta.
