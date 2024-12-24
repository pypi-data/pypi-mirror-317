import numpy as np

def incidence_matrix(graph): # Вычисляет матрицу инцидентности неориентированного графа.
# graph: Словарь, представляющий граф. Ключи — вершины, значения — списки смежных вершин.

  nodes = sorted(graph.keys())
  edges = set()
  for node in graph:
    for neighbor in graph[node]:
      edge = tuple(sorted((node, neighbor))) # Создаем кортеж
      edges.add(edge)
  edges = list(edges)

  num_nodes = len(nodes)
  num_edges = len(edges)
  inc_matrix = np.zeros((num_nodes, num_edges), dtype=int)

  for j, edge in enumerate(edges):
      i1 = nodes.index(edge[0])
      i2 = nodes.index(edge[1])
      inc_matrix[i1, j] = 1
      inc_matrix[i2, j] = 1

  return inc_matrix # Возвращаем матрицу инцидентности в виде NumPy массива

if __name__ == '__main__':
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    inc_matrix = incidence_matrix(graph)
    print("\nМатрица инцидентности:")
    print(inc_matrix)