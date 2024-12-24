def dijkstra(graph, start):
    # Инициализация кратчайших расстояний: все вершины, кроме начальной, равны бесконечности
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # Инициализация очереди, в которой будем хранить вершины, которые нужно посетить
    queue = [start]

    while queue:
        current_vertex = queue.pop(0)

        # Просмотр соседей текущей вершины и обновление кратчайших расстояний до них
        for neighbor in graph[current_vertex]:
            distance = distances[current_vertex] + graph[current_vertex][neighbor]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                queue.append(neighbor)

    return distances

if __name__ == '__main__':
    # Пример графа в виде словаря с весами ребер
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }

    start_vertex = 'A'
    shortest_distances = dijkstra(graph, start_vertex)

    print(shortest_distances)
