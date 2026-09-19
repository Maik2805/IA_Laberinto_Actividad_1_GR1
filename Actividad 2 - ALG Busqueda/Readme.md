# Laberinto con Algoritmos de Búsqueda

Programa que construye un laberinto como grafo y lo resuelve automáticamente usando **BFS** o **DFS**, según elija el usuario. Muestra el proceso de exploración y la ruta encontrada de forma visual.

#### **Readme construido con herramienta de IA.**
---

## Archivos

| Archivo | Descripción |
|---|---|
| `laberinto_con_busqueda.py` | Programa principal |
| `BFS.py` | Referencia de implementación BFS |
| `DFS.py` | Referencia de implementación DFS |

---

## Requisitos

```
pip install networkx matplotlib
```

---

## Ejecución

```bash
python laberinto_con_busqueda.py
```

---

## Cómo funciona

### 1. Definición del laberinto

El laberinto es una matriz 9×9 con tres tipos de celda:

| Valor | Significado |
|---|---|
| `0` | Camino libre |
| `1` | Pared (bloqueado) |
| `9` | Meta |

El inicio siempre es la celda `(0, 0)`. La posición de la meta se detecta automáticamente buscando el valor `9` en la matriz — se puede mover libremente sin tocar ninguna otra parte del código.

### 2. Construcción del grafo

A partir de la matriz se construye un grafo no dirigido con `networkx`:

- Cada celda con valor `0` o `9` se convierte en un **nodo**, identificado por su coordenada `(fila, columna)`.
- Se crean **aristas** entre nodos adyacentes (arriba, abajo, izquierda, derecha) que no sean pared.

### 3. Selección del algoritmo

El programa pregunta al usuario por consola:

```
(1) BFS — Búsqueda en Anchura
(2) DFS — Búsqueda en Profundidad
```

### 4. Algoritmos de búsqueda

Ambos algoritmos reciben el grafo, el nodo de inicio y el nodo meta, y devuelven la **ruta encontrada** y el **orden de exploración**.

#### BFS — Búsqueda en Anchura

Usa una **cola FIFO** (`pop(0)`). Explora nivel por nivel, por lo que **garantiza la ruta con el menor número de pasos**.

```
cola = [inicio]
mientras cola no esté vacía:
    extraer el primero  ← FIFO
    si es la meta → reconstruir camino y retornar
    agregar vecinos no visitados al final de la cola
```

#### DFS — Búsqueda en Profundidad

Usa una **pila LIFO** (`pop(-1)`). Sigue una rama hasta el fondo antes de retroceder. **No garantiza la ruta más corta**, pero puede ser más rápido en laberintos donde la meta está en una rama profunda.

```
pila = [inicio]
mientras pila no esté vacía:
    extraer el último  ← LIFO
    si es la meta → reconstruir camino y retornar
    agregar vecinos no visitados al final de la pila
```

Ambos usan un diccionario `predecesor` para reconstruir el camino desde la meta hasta el inicio al finalizar.

### 5. Resultados en consola

```
--- Resultado BFS ---
  Ruta encontrada (7 pasos):
  (0, 0) → (1, 0) → (2, 0) → ... → (3, 4)
  Nodos explorados: 22
  Orden de exploración: [(0, 0), (1, 0), ...]
```

### 6. Visualización

El programa abre dos ventanas de matplotlib:

**Figura 1 — Estado inicial**

Muestra el grafo del laberinto antes de ejecutar ningún algoritmo.

| Color | Nodo |
|---|---|
| Naranja | Inicio `(0, 0)` |
| Verde | Meta |
| Gris claro | Camino libre |

**Figura 2 — Resultado**

Muestra el grafo después de ejecutar el algoritmo seleccionado.

| Color | Nodo |
|---|---|
| Azul (`steelblue`) | Explorado durante la búsqueda |
| Verde (`limegreen`) | Forma parte de la ruta encontrada |
| Naranja | Inicio |
| Rojo | Meta alcanzada |
| Gris claro | No visitado |

Las aristas de la ruta se pintan en verde con mayor grosor.

> Cierra cada ventana para continuar con el siguiente paso del programa.

---

## Nota sobre el orden de exploración

El `orden_visita` registra el momento en que un nodo es **descubierto** (encolado/apilado), no cuando es extraído. Por eso es posible que la meta aparezca en la lista seguida de otros nodos: esos nodos ya habían sido encolados en iteraciones anteriores antes de que el algoritmo extrajera y verificara la meta. La ruta devuelta es siempre correcta.
