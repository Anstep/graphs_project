from collections import deque
from heapq import heappop, heappush
from math import inf

import numpy as np


class Graph:
    # переписать инициализацию через декораторы
    def __init__(
        self,
        vertices_count: int,
        adj_matrix=None,
        adj_list=None,
        inc_matrix=None,
        adj_matrix_weighted=None,
        adj_list_weighted=None,
    ):
        self.v_count = vertices_count
        if adj_matrix is not None:
            self.adj_matrix = np.array(adj_matrix, dtype=int)
        elif adj_list is not None:
            self.adj_matrix = np.zeros((vertices_count, vertices_count), dtype=int)
            for vertex, neighbors_list in adj_list.items():
                for neighbor in neighbors_list:
                    self.adj_matrix[vertex][neighbor] = 1
        elif inc_matrix is not None:
            pass
        elif adj_list_weighted:
            for vertex, neighbors_list_w in adj_list_weighted.items():
                for neighbor, weight in neighbors_list_w:
                    self.adj_matrix[vertex][weight] = weight
        else:
            self.adj_matrix = np.zeros((vertices_count, vertices_count), dtype=int)

    def get_adj_list(self):
        adj_list = {i: [] for i in range(self.v_count)}
        for i in range(self.v_count):
            for j in range(self.v_count):
                if self.adj_matrix[i][j]:
                    adj_list[i].append(j)
        return adj_list

    def get_adj_list_weighted(self):
        adj_list = {i: [] for i in range(self.v_count)}
        for i in range(self.v_count):
            for j in range(self.v_count):
                adj_list[i].append((j, self.adj_matrix[i][j]))
        return adj_list

    # Задача 0
    def get_vertex_degrees(self):
        adj_list = self.get_adj_list()
        vertex_degrees = [0] * self.v_count
        for vertex, neighbors in adj_list.items():
            vertex_degrees[vertex] = len(neighbors)
        return vertex_degrees

    def get_eulerian_status(self):
        pass

    def get_bipartite_status(self):
        pass

    # Задача 1
    def get_dfs(self, start_vertex):
        pass

    # Задача 2
    def verify_dfs(self, user_path):
        # Не учитывает несколько компонент связности,
        # использует O(n) проверку
        adj_list = self.get_adj_list()
        stack = []
        visited = [False] * len(adj_list)

        def verification_dfs(user_path):
            if not user_path:
                return True

            # if len(user_path) >= self.v_count:
            #     return False

            visited[user_path[0]] = True
            stack.append(user_path[0])
            found = False
            for next_node in range(1, len(user_path)):
                next_node = user_path[next_node]
                found = False
                while stack:
                    cur_node = stack[-1]
                    if next_node in adj_list[cur_node]:
                        if not visited[next_node]:
                            visited[next_node] = True
                            stack.append(next_node)
                            found = True
                            break
                        else:
                            return False
                    else:
                        stack.pop()
                if not found:
                    return False
            return True

        return verification_dfs(user_path)

    # Задача 3
    def get_bfs(self, start_vertex):
        pass

    # Задача 4
    def verify_bfs(self, user_path):
        # Главные условия
        # 1. Если у начала очереди есть непосещенные вершины, то след. в. должна быть из этого списка
        # 2. Переход к следующей в. в очереди только после посещения всех соседей

        # def bfs(vertex):
        #     queue = deque()
        #     queue.append(vertex)
        #     d = [-1] * self.v_count
        #     d[vertex] = 0
        #     while queue:
        #         vertex = queue.popleft()
        #         for neighbor in adj_list[vertex]:
        #             if d[neighbor] == -1:
        #                 queue.append(neighbor)
        #                 d[neighbor] = d[vertex] + 1
        #     print(d)

        if not user_path:
            return True

        adj_list = self.get_adj_list()
        start_vertex = user_path[0]

        queue = deque()
        visited = [False] * len(adj_list)
        visited[start_vertex] = True
        queue.append(start_vertex)
        i_path = 1
        while queue and i_path < len(user_path):
            next_node = user_path[i_path]

            unvisited_neighbors = [
                vertex for vertex in adj_list[queue[0]] if not visited[vertex]
            ]

            if next_node in unvisited_neighbors:
                visited[next_node] = True
                queue.append(next_node)
                i_path += 1
            else:
                if unvisited_neighbors:
                    return False
                queue.popleft()
        return i_path == len(user_path)

    # Задача 5
    def get_connected_components_count(self):
        pass

    # Задача 6
    def verify_components_count(self, user_count):
        return True if self.get_connected_components_count() else False

    # Задача 7
    def get_minimal_spanning_tree(self):
        pass

    # Задача 8
    def get_shortest_paths_from(self, start_vertex):
        adj_list = self.get_adj_list_weighted()
        d = [inf] * self.v_count
        marked = [False] * self.v_count
        d[start_vertex] = 0
        for _ in range(self.v_count):
            cur_vertex = -1
            for i in range(self.v_count):
                if not marked[i] and (cur_vertex == -1 or d[i] < d[cur_vertex]):
                    cur_vertex = i
            if cur_vertex == -1 or d[cur_vertex] == inf:
                break
            marked[cur_vertex] = True
            for vertex, weight in adj_list[cur_vertex]:
                if weight > 0:
                    d[vertex] = min(d[vertex], d[cur_vertex] + weight)
        return [int(val) if val != inf else -1 for val in d]

    # Задача 9
    def get_matrix_shortest_paths(self):
        pass

    # Задача 10
    def encode_prufer(self):
        # https://cp-algorithms.com/graph/pruefer_code.html
        adj_list = self.get_adj_list()
        n = len(adj_list)
        leafs = list()
        degree = [0] * n
        used = [False] * n
        for i in range(n):
            degree[i] = len(adj_list[i])
            if degree[i] == 1:
                heappush(leafs, i)
        code = [-1] * (n - 2)
        for i in range(n - 2):
            leaf = heappop(leafs)
            used[leaf] = True
            digit = 0
            for digit_candidate in adj_list[leaf]:
                if not used[digit_candidate]:
                    digit = digit_candidate
            # digit = adj_list[leaf][0]
            code[i] = digit
            degree[digit] -= 1
            if degree[digit] == 1:
                heappush(leafs, digit)
        return code

    # Задача 11
    @staticmethod
    def decode_prufer(code):
        pass

    # Задача 12
    def get_coloring(self):
        pass


"""
# --- Тест 1: Валидный DFS с глубоким бектрекингом ---
# Граф: 0-1, 0-2, 2-3, 3-4
# Путь: [0, 1, 2, 3, 4]
# Ожидаемый результат: True (0->1, тупик, возврат к 0, 0->2->3->4)
adj_matrix1 = [
    [0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0],
]
test_graph1 = Graph(vertices_count=5, adj_matrix=adj_matrix1)
print(f"Test 1 (Valid Backtrack): {test_graph1.verify_dfs([0, 1, 2, 3, 4])}")

# --- Тест 2: Невалидный DFS (Прыжок) ---
# Граф: 0-1, 1-2, 3-4 (две изолированные компоненты 0-1-2 и 3-4)
# Путь: [0, 1, 3]
# Ожидаемый результат: False (Узел 3 недостижим из стека [0, 1])
adj_matrix2 = [
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0],
]
test_graph2 = Graph(vertices_count=5, adj_matrix=adj_matrix2)
print(f"Test 2 (Unreachable jump): {test_graph2.verify_dfs([0, 1, 3])}")

# --- Тест 3: Невалидный DFS (Повторное посещение / Цикл) ---
# Граф: 0-1, 1-2, 2-0 (треугольник)
# Путь: [0, 1, 2, 0]
# Ожидаемый результат: False (DFS не должен включать уже посещенный узел в user_path)
adj_matrix3 = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
test_graph3 = Graph(vertices_count=3, adj_matrix=adj_matrix3)
print(f"Test 3 (Cycle/Visited): {test_graph3.verify_dfs([0, 1, 2, 0])}")

# --- Тест 4: Сложный граф (Неявный бектрекинг) ---
# Граф: 0-1, 0-2, 1-3
# Путь: [0, 1, 3, 2]
# Ожидаемый результат: True (0->1->3, возврат к 1, возврат к 0, 0->2)
adj_matrix4 = [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
test_graph4 = Graph(vertices_count=4, adj_matrix=adj_matrix4)
print(f"Test 4 (Deep valid): {test_graph4.verify_dfs([0, 1, 3, 2])}")

# --- Тест 5: Нарушение структуры стека ---
# Граф: 0-1, 1-2, 0-3
# Путь: [0, 1, 3, 2]
# Ожидаемый результат: False (После 1->3 узел 2 не может быть посещен, так как он сосед 1,
# но 1 уже вытолкнут из стека попыткой найти соседа для 3)
adj_matrix5 = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
test_graph5 = Graph(vertices_count=4, adj_matrix=adj_matrix5)
print(f"Test 5 (Stack violation): {test_graph5.verify_dfs([0, 1, 3, 2])}")
"""

# # --- Тест 14: Взвешенный граф (Простой треугольник) ---
# # 0-1 (вес 5), 1-2 (вес 10), 0-2 (вес 1)
# # От 0: [0, 5, 1]
# adj_matrix14 = [
#     [0, 5, 1],
#     [5, 0, 10],
#     [1, 10, 0],
# ]
# test_graph14 = Graph(vertices_count=3, adj_matrix=adj_matrix14)
# print(f"Test 14 (Weighted triangle): {test_graph14.get_shortest_paths_from(0)}")

# # --- Тест 15: Взвешенный граф (Выбор более длинного пути по количеству ребер) ---
# # 0-1 (10), 0-2 (1), 2-1 (1)
# # От 0: [0, 2, 1] (путь 0-2-1 короче чем 0-1)
# adj_matrix15 = [
#     [0, 10, 1],
#     [10, 0, 1],
#     [1, 1, 0],
# ]
# test_graph15 = Graph(vertices_count=3, adj_matrix=adj_matrix15)
# print(f"Test 15 (Weighted shortcut): {test_graph15.get_shortest_paths_from(0)}")

# # --- Тест 16: Сложный взвешенный граф (6 вершин) ---
# # 0-1(7), 0-2(9), 0-5(14), 1-2(10), 1-3(15), 2-3(11), 2-5(2), 3-4(6), 4-5(9)
# adj_matrix16 = [
#     [0, 7, 9, 0, 0, 14],
#     [7, 0, 10, 15, 0, 0],
#     [9, 10, 0, 11, 0, 2],
#     [0, 15, 11, 0, 6, 0],
#     [0, 0, 0, 6, 0, 9],
#     [14, 0, 2, 0, 9, 0],
# ]
# test_graph16 = Graph(vertices_count=6, adj_matrix=adj_matrix16)
# # От 0: [0, 7, 9, 20, 20, 11]
# print(f"Test 16 (Complex weighted): {test_graph16.get_shortest_paths_from(0)}")

# # --- Тест 17: Взвешенный несвязный граф ---
# adj_matrix17 = [
#     [0, 2, 0, 0],
#     [2, 0, 0, 0],
#     [0, 0, 0, 4],
#     [0, 0, 4, 0],
# ]
# test_graph17 = Graph(vertices_count=4, adj_matrix=adj_matrix17)
# # От 0: [0, 2, -1, -1]
# print(f"Test 17 (Disconnected weighted): {test_graph17.get_shortest_paths_from(0)}")

# # --- Тест 18: Граф с "ловушкой" (большие веса) ---
# # 0-1(100), 1-2(100), 0-2(201)
# # От 0: [0, 100, 200]
# adj_matrix18 = [
#     [0, 100, 201],
#     [100, 0, 100],
#     [201, 100, 0],
# ]
# test_graph18 = Graph(vertices_count=3, adj_matrix=adj_matrix18)
# print(f"Test 18 (Weighted trap): {test_graph18.get_shortest_paths_from(0)}")

# --- Тест 19: Код Прюфера (Звезда K_1,4) ---
# Центр в 0, листья 1, 2, 3, 4
# Ожидаемый результат: [0, 0, 0]
# adj_matrix19 = [
#     [0, 1, 1, 1, 1],
#     [1, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0],
# ]
# test_graph19 = Graph(vertices_count=5, adj_matrix=adj_matrix19)
# print(f"Test 19 (Star Prufer): {test_graph19.encode_prufer()}")

# # --- Тест 20: Код Прюфера (Путь P_5) ---
# # 0-1-2-3-4
# # Ожидаемый результат: [1, 2, 3]
# adj_matrix20 = [
#     [0, 1, 0, 0, 0],
#     [1, 0, 1, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 1, 0, 1],
#     [0, 0, 0, 1, 0],
# ]
# test_graph20 = Graph(vertices_count=5, adj_matrix=adj_matrix20)
# print(f"Test 20 (Path Prufer): {test_graph20.encode_prufer()}")

# # --- Тест 21: Код Прюфера (Минимальное дерево) ---
# # 0-1
# # Ожидаемый результат: [] (для n=2 длина n-2=0)
# adj_matrix21 = [[0, 1], [1, 0]]
# test_graph21 = Graph(vertices_count=2, adj_matrix=adj_matrix21)
# print(f"Test 21 (Minimal Prufer): {test_graph21.encode_prufer()}")

# # --- Тест 22: Код Прюфера (Разветвленное дерево) ---
# # Ребра: (0,1), (0,2), (1,3), (1,4)
# # Ожидаемый результат: [0, 1, 1]
# adj_matrix22 = [
#     [0, 1, 1, 0, 0],
#     [1, 0, 0, 1, 1],
#     [1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 0, 0],
# ]
# test_graph22 = Graph(vertices_count=5, adj_matrix=adj_matrix22)
# print(f"Test 22 (Branched Prufer): {test_graph22.encode_prufer()}")

# # --- Тест 23: Код Прюфера (Сложное дерево) ---
# # Ребра: (0,1), (0,2), (1,3), (1,4), (2,5), (2,6)
# # Ожидаемый результат: [1, 1, 0, 2, 2]
# adj_matrix23 = [
#     [0, 1, 1, 0, 0, 0, 0],
#     [1, 0, 0, 1, 1, 0, 0],
#     [1, 0, 0, 0, 0, 1, 1],
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0],
# ]
# test_graph23 = Graph(vertices_count=7, adj_matrix=adj_matrix23)
# print(f"Test 23 (Complex Prufer): {test_graph23.encode_prufer()}")
