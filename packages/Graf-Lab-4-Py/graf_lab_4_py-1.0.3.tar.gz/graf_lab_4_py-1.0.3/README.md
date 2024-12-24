# Graf: Библиотека для работы с графами и алгоритмами

**Graf** - это библиотека Python, предоставляющая инструменты для работы с графами и реализации различных алгоритмов на них. Она включает в себя алгоритмы Дейкстры, Флойда-Уоршалла, поиска Эйлерова цикла, а также возможность читать и визуализировать графы из файлов формата DOT.

## Установка

Для установки `Graf-Lab-4-Py`, используйте `pip`:

`pip install Graf-Lab-4-Py`

## Зависимости

Graf зависит от следующих библиотек:

-   networkx - для работы с графами, например для создания, добавления ребер, расположения узлов и отображения.
-   matplotlib - для визуализации графов.
-   numpy - для хранения и манипулирования числовыми данными (матрицами) для графов.

Эти зависимости будут установлены автоматически при установке пакета с помощью pip. # Будут же?

## Модули

Библиотека состоит из следующих модулей:

•   Graf.Algorithm.floyd_warshall: Реализация алгоритма Уоршалла-Флойда.

•   Graf.Algorithm.dijkstra: Реализация алгоритма Дейкстры.

•   Graf.Algorithm.euler: Реализация нахождение Эйлерова цикла.

•   Graf.Matrix.Vis_matrix: Реализация базовой структуры графа с помощью класса Graph (c методами для добавления ребер) и вывода матрицы весов.

•   Graf.Matrix.Incidence_matrix: Реализация вывода матрици инцидентности.

•   Graf.Matrix.Adjacency_matrix: Реализация вывода матрици смежности.


## Использование

### Алгоритм Дейкстры

```
python
from Graf.Algorithm.dijkstra import dijkstra

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_vertex = 'A'
shortest_distances = dijkstra(graph, start_vertex)

print(shortest_distances) # Выведет {'A': 0, 'B': 1, 'C': 3, 'D': 4}
```

### Алгоритм Уоршалла-Флойда

Для работы алгоритма необходимо создать файл graph.dot с описанием графа в формате DOT

**Пример:** u -> v [label="w"], где u - начальная вершина, v - целевая вершина, w - вес ребра
```
# digraph G {
#   1 -> 2 [label="5"];
#   2 -> 3 [label="1"];
#   3 -> 1 [label="2"];
# }
```

```
python
from Graf.floyd_warshall import floyd_warshall
from Graf.graph_utils import read_graph_from_dot

graph = read_graph_from_dot("graph.dot")
shortest_paths = floyd_warshall(graph)

# Результат в shortest_paths - матрица кратчайших расстояний
with open("shortest_paths.txt", 'w', encoding='utf-8') as f:
    for i in range(len(graph)):
        for j in range(len(graph)):
            if shortest_paths[i][j] == float('inf'):
                f.write(f"Расстояние от {i + 1} до {j + 1}: ∞\n")
            else:
                f.write(f"Расстояние от {i + 1} до {j + 1}: {shortest_paths[i][j]}\n")
print("Кратчайшие пути (Флойд-Уоршалл) записаны в shortest_paths.txt")
```

### Нахождениие Эйлерова цикла

```
# Находим Эйлеров цикл
eulerian_cycle = find_eulerian_cycle(graph, start_vertex)

# Вывод результата
if eulerian_cycle:
    print("Эйлеров цикл:", eulerian_cycle)
else:
    print("Эйлеров цикл не существует.")


```

### Визуализация графа для алгоритм Уоршалла-Флойда

Для визуализации графа необходимо прочитать его из файла .dot.

```
python
from Graf.floyd_warshall import read_graph_from_dot, draw_graph

graph = read_graph_from_dot("graph.dot")
draw_graph(graph)
```

### Вывод матрици весов 

```
python
g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 15)
g.add_edge(1, 2, 20)
g.add_edge(2, 3, 30)

# выводим матрицу весов
g.print_matrix()
```

### Вывод матрици инцидентности

```
python
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
```

### Вывод матрици смежности 

```
python
g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 15)
g.add_edge(1, 2, 20)
g.add_edge(2, 3, 30)

# выводим матрицу весов
g.print_matrix()
```

## Автор

•   Садова Диана
•   Жукова Арина

## Лицензия

Этот проект лицензирован под MIT License.

## Дополнительная информация

Пожалуйста, посетите страницу проекта на [GitHub](https://github.com/DianaSadova/Graf) для получения дополнительной информации и кода.
