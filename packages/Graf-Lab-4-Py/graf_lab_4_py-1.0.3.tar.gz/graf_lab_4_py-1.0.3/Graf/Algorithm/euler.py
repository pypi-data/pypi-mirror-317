
# Проверяем все ли вершины имеют четную степень
def is_eulerian(graph):
    for edges in graph.values():
        if len(edges) % 2 != 0:
            return False
    return True

def find_eulerian_cycle(graph, start):
    if not is_eulerian(graph):
        return None

    # Копируем граф, чтобы не изменять оригинал
    graph_copy = {node: edges[:] for node, edges in graph.items()}
    cycle = []  # для хранения найденного цикла
    stack = [start]  # для реализации алгоритма обхода в глубину

    while stack:
        current = stack[-1]
        if graph_copy[current]:  # Если у текущей вершины есть смежные вершины
            next_node = graph_copy[current].pop()  # Берем случайное ребро
            graph_copy[next_node].remove(current)  # Удаляем обратное ребро
            stack.append(next_node)  # Добавляем следующую вершину в стек
        else:  # Если у текущей вершины нет смежных вершин
            cycle.append(stack.pop())  # Добавляем текущую вершину в цикл и удаляем её из стека

    return cycle[::-1]  # Возвращаем цикл в правильном порядке

if __name__ == '__main__':
    graph = {1:[2,5],
             2:[1,3,4,5],
             3:[2,6],
             4:[2,5],
             5:[1,2,4,6],
             6:[3,5]}
    start_vertex = int(input("Введите начальную вершину (1-6): "))

    # Находим Эйлеров цикл
    eulerian_cycle = find_eulerian_cycle(graph, start_vertex)

    # Вывод результата
    if eulerian_cycle:
        print("Эйлеров цикл:", eulerian_cycle)
    else:
        print("Эйлеров цикл не существует.")
