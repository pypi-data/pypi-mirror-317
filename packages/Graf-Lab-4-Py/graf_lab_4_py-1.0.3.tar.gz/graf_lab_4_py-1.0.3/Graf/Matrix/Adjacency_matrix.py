import numpy as np

def adjacency_matrix(graph): # Вычисляет матрицу смежности неориентированного графа.
# graph: Словарь, представляющий граф. Ключи — вершины, значения — списки смежных вершин.

    nodes = sorted(graph.keys())
    num_nodes = len(nodes)
    adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    for i, node1 in enumerate(nodes):
        for node2 in graph[node1]:
            j = nodes.index(node2)
            adj_matrix[i, j] = 1  # Неориентированный граф: ребро в обе стороны
            adj_matrix[j, i] = 1

    return adj_matrix # Возвращаем матрица смежности в виде NumPy массива.

if __name__ == '__main__':
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }

    # Вычисление и вывод матрицы смежности
    adj_matrix = adjacency_matrix(graph)
    print("Матрица смежности:")
    print(adj_matrix)


