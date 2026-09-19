grafo = {
    'V': ['J'],
    'J': ['D', 'V'],
    'D': ['J','I','K','A','C'],
    'K': ['D','M'],
    "I": ["D"],
    'A': ['D','C','B','E'],
    'C': ['D','A','M','L','U'],
    'M': ['K','C'],
    'L': ['C','Y','Z'],
    'Y': ['L'],
    'Z': ['L'],
    'B': ['A','F','G','H'],
    'F': ['B','R'],
    'G': ['B'],
    'H': ['B','S','T','U'],
    'R': ['F'],
    'S': ['H'],
    'T': ['H'],
    'U': ['H','C'],
    'E': ['A','N','O'],
    'N': ['E'],
    'O': ['E']
}
def bfs_camino(grafo, inicio, objetivo):
    cola = [inicio]
    visitados = {inicio}
    predecesor = {inicio: None}
    while cola:
        nodo = cola.pop(0)
        if nodo == objetivo:
            # reconstrucción del camino
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = predecesor[nodo]
            return list(reversed(camino))
        
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                cola.append(vecino) 
    return None
camino=bfs_camino(grafo, "K", "U")
print(camino)