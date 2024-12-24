import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def floyd_warshall(graph):
    n = len(graph)
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif graph[i][j] != float('inf'):
                dist[i][j] = graph[i][j]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# Чтение весов из файла
def read_graph_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Преобразование строк в матрицу
    graph = np.full((113, 113), float('inf'))
    for i, line in enumerate(lines):
        row = line.strip().split()
        for j, value in enumerate(row):
            if value != 'inf':
                graph[i][j] = float(value)

    return graph


# Визуализация графа с помощью NetworkX
def draw_graph(graph):
    num_nodes = graph.shape[0]
    edges = []

    # Создаем ребра, игнорируя значения inf
    for i in range(num_nodes):
        for j in range(num_nodes):
            if graph[i][j] != float('inf'):
                edges.append((i, j, graph[i][j]))

    # Создаем ориентированный граф
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)

    # Корректировка меток вершин
    labels = {i: str(i + 1) for i in range(num_nodes)}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight='bold')

    nx.draw_networkx_edges(G, pos)

    # Подготовка меток для ребер
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Граф ")
    plt.axis('off')  # Отключаем оси
    plt.show()


# Чтение графа из файла DOT
def read_graph_from_dot(filename):
    graph = np.full((113, 113), float('inf'))  # предположим, что у нас 113 узлов

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            # Ищем ребра, которые имеют формат "u -> v [label=w];"
            if '->' in line:
                parts = line.split('->')
                left = parts[0].strip().strip('"')  # Удаляем кавычки у узла
                right = parts[1].strip().strip('";')  # Удаляем кавычки и точку с запятой

                # Извлечение номера узла
                node_from = int(left) - 1  # преобразуем в индекс

                # Извлечение узла назначения и атрибутов
                node_to_parts = right.split('[')
                node_to = int(node_to_parts[0].strip().strip('"')) - 1  # Удаляем кавычки
                weight = 1.0  # значение веса по умолчанию

                # Если указаны атрибуты, извлекаем вес
                if len(node_to_parts) > 1:
                    for attr in node_to_parts[1:]:
                        if 'label' in attr:  # Если найден вес в атрибуте label
                            weight_str = attr.split('=')[1].strip().strip('"\']')  # Удаляем кавычки
                            weight = float(weight_str) if weight_str != 'inf' else float('inf')
                            break

                graph[node_from][node_to] = weight

    return graph


# Основная логика программы
if __name__ == "__main__":
    graph = read_graph_from_dot("graph.dot")  # Замените "graph.dot" на имя вашего файла
    shortest_paths = floyd_warshall(graph)

    # Вывод результатов в файл
    with open("shortest_paths.txt", 'w', encoding='utf-8') as f:
        for i in range(len(graph)):
            for j in range(len(graph)):
                if shortest_paths[i][j] == float('inf'):
                    f.write(f"Расстояние от {i + 1} до {j + 1}: ∞\n")
                else:
                    f.write(f"Расстояние от {i + 1} до {j + 1}: {shortest_paths[i][j]}\n")
    print("Матрица графа:")
    print(graph)
    # Визуализация графа
    draw_graph(graph)
