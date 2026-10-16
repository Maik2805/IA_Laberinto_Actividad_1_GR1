# Laberinto con Algoritmos de Búsqueda

Dos programas que modelan un laberinto como un grafo y lo resuelven automáticamente usando **BFS**, **DFS** o **UCS**, según elija el usuario. Ambos muestran el proceso de exploración y la ruta encontrada por consola y de forma visual.

#### **Readme construido con herramienta de IA.**
---

## Archivos

| Archivo | Descripción |
|---|---|
| `laberinto_con_busqueda.py` | Versión basada en **matriz**: el grafo se construye automáticamente a partir de una matriz del laberinto. |
| `laberinto_lista_adyacencia.py` | Versión basada en **lista de adyacencia**: el grafo y los costos se definen de forma explícita. |

Ambos programas resuelven el mismo laberinto y ofrecen los mismos algoritmos. Se diferencian en cómo representan el grafo.

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

Versión por matriz:

```bash
python laberinto_con_busqueda.py
```

Versión por lista de adyacencia:

```bash
python laberinto_lista_adyacencia.py
```

Al ejecutar cualquiera de los dos, el programa muestra el grafo inicial, pide elegir un algoritmo y luego muestra la ruta encontrada.

---

## Las dos representaciones del grafo

### `laberinto_con_busqueda.py` — a partir de una matriz

El laberinto se define como una matriz donde cada valor indica el tipo de celda:

| Valor | Significado | Costo |
|---|---|---|
| `0` | Camino libre | 4 |
| `1` | Pared (bloqueado) | — |
| `2` | Premio | 1 |
| `3` | Penalización | 12 |
| `9` | Meta | 4 |

El grafo se construye solo: cada celda que no es pared se convierte en un **nodo** `(fila, columna)` y se conecta con sus vecinos transitables. El costo de cada arista se deriva del tipo de la celda destino. El inicio es `(0, 0)` y la meta (el `9`) se detecta automáticamente.

Esta versión es la más **intuitiva de leer**, porque el laberinto se ve directamente en el código.

### `laberinto_lista_adyacencia.py` — lista de adyacencia

Aquí el grafo se define como un diccionario donde cada nodo lista sus vecinos junto con el **costo explícito** de cada arista:

```python
grafo = {
    "A": [("I", 4), ("B", 4)],
    "B": [("A", 4), ("C", 4)],
    ...
}
```

Los nodos se identifican con letras (`A`, `B`, ... `Z`, `AA`, `AB`, ...). Esta versión se adoptó para **definir los costos sin ambigüedad**: en un grafo no dirigido construido desde matriz, el costo (que es propiedad de la celda) no se traslada de forma única a la arista. Con la lista de adyacencia el costo se escribe directamente sobre cada conexión y puede editarse a mano.

Para cambiar un costo, basta modificar el número en la tupla correspondiente.

---

## Algoritmos de búsqueda

Al ejecutar, el programa pregunta:

```
(1) BFS — Búsqueda en Anchura (menos pasos)
(2) DFS — Búsqueda en Profundidad
(3) UCS — Búsqueda de Costo Uniforme (menor costo)
(0) Salir del programa
```

Los tres reciben el grafo, el inicio y la meta, y devuelven la **ruta encontrada** y el **orden de exploración**.

### BFS — Búsqueda en Anchura

Usa una **cola FIFO** (`pop(0)`). Explora nivel por nivel, por lo que garantiza la ruta con el **menor número de pasos**. No tiene en cuenta los costos.

### DFS — Búsqueda en Profundidad

Usa una **pila LIFO** (`pop(-1)`). Sigue una rama hasta el fondo antes de retroceder. **No garantiza** la ruta más corta ni la más barata.

### UCS — Búsqueda de Costo Uniforme

Usa una **cola de prioridad** ordenada por costo acumulado: siempre expande el nodo alcanzable con menor costo total. Garantiza la ruta de **menor costo** usando el peso de las aristas.

Los tres comparten la misma mecánica: un contenedor de nodos pendientes, un registro de visitados y un diccionario `predecesor` para reconstruir el camino. La diferencia está en **cómo eligen el siguiente nodo**: cola, pila o prioridad por costo.

---

## Resultados en consola

```
--- Resultado UCS ---
  Ruta encontrada (13 pasos):
  A → I → M → N → ... → AO
  Costo total de la ruta: 57
  Nodos explorados: 53
  Orden de exploración: [A, I, B, ...]
```

---

## Visualización

El programa abre dos ventanas de matplotlib:

**Figura 1 — Estado inicial.** El grafo antes de resolver.

| Color | Nodo |
|---|---|
| Naranja | Inicio |
| Verde | Meta |
| Dorado | Premio |
| Rojo claro | Penalización |
| Gris claro | Camino libre |

**Figura 2 — Resultado.** El grafo tras ejecutar el algoritmo elegido.

| Color | Nodo |
|---|---|
| Azul | Explorado durante la búsqueda |
| Verde | Forma parte de la ruta encontrada |
| Naranja | Inicio |
| Rojo | Meta alcanzada |
| Gris claro | No visitado |

Las aristas muestran su costo como etiqueta, y las de la ruta se pintan en verde con mayor grosor.

> Cierra cada ventana para continuar con el siguiente paso del programa.

---

## Nota sobre el orden de exploración

El `orden_visita` registra el momento en que un nodo es **descubierto** (encolado o apilado), no cuando es explorado. Por eso la meta puede aparecer en la lista seguida de otros nodos: esos nodos ya habían sido encolados en iteraciones anteriores antes de que el algoritmo extrajera y verificara la meta. La ruta devuelta es siempre correcta.
