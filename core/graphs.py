from abc import ABC, abstractmethod


class BaseGraph(ABC):
    def __init__(self, storage):
        self._storage = storage

    @property
    @abstractmethod
    def is_directed(self):
        pass

    def get_vertices_count(self) -> int:
        return self._storage.get_vertices_count()

    def get_neighbors(self, v) -> list[tuple[int, int]]:
        return self._storage.get_neighbors(v)

    def is_edge(self, u, v) -> bool:
        return self._storage.is_edge(u, v)


class UndirectedGraph(BaseGraph):
    def is_directed(self):
        return False

    def get_degree(self, u):
        return len(self._storage.get_neighbors(u))


class DirectedGraph(BaseGraph):
    def is_directed(self):
        return True

    def get_in_degree(self, u):
        pass

    def get_out_degree(self, u):
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
