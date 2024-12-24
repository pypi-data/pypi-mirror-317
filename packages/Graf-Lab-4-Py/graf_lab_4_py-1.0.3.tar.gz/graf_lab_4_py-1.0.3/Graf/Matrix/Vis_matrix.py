class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight  # для неориентированного графа

    def add_edge_directed(self, u,v,weight): # для ориентированного графа
        self.graph[u][v] = weight

    def print_matrix(self):
        for i in range(self.V):
            for j in range(self.V):
                print(self.graph[i][j], end=" ")
            print()

if __name__ == '__main__':
    # создаем граф с 4 вершинами
    g = Graph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 15)
    g.add_edge(1, 2, 20)
    g.add_edge(2, 3, 30)

    # выводим матрицу весов
    g.print_matrix()
    print("--------------------")
    g = Graph(4)
    g.add_edge_directed(0, 1, 10)
    g.add_edge_directed(0, 2, 15)
    g.add_edge_directed(1, 2, 20)
    g.add_edge_directed(2, 3, 30)

    # выводим матрицу весов
    g.print_matrix()
