from abc import ABC, abstractmethod

import numpy as np


class GraphStorage(ABC):
    @abstractmethod
    def add_edge(self, u, v, w):
        pass

    @abstractmethod
    def is_edge(self, u, v):
        pass

    @abstractmethod
    def get_vertices_count(self):
        pass

    @abstractmethod
    def get_neighbors(self, u):
        pass

    @abstractmethod
    def get_adj_matrix(self):
        pass


class AdjacencyMatrixStorage(GraphStorage):
    def __init__(self, matrix):
        self.adj_matrix = np.array(matrix, dtype="float")

    def add_edge(self, u, v, w=1):
        self.adj_matrix[u, v] = w

    def is_edge(self, u, v):
        return True if self.adj_matrix[u, v] else False

    def get_vertices_count(self):
        return self.adj_matrix.shape[0]

    def get_neighbors(self, u):
        row = self.adj_matrix[u]
        # Возвращает кортеж
        inds = np.where(row != 0)[0]

        weights = row[inds]
        # tolist для конвертирования в стандартные типы
        return list(zip(inds.tolist(), weights.tolist()))

    def get_adj_matrix(self):
        return self.adj_matrix.copy()


class AdjacencyListStorage(GraphStorage):
    def __init__(self, adj_list):
        # копирование
        self.adj_list = {u: list(neighbors) for u, neighbors in adj_list.items()}

    def add_edge(self, u, v, w=1):
        self.adj_list[u].append((v, w))

    def is_edge(self, u, v):
        for neighbor, _ in self.adj_list[u]:
            if neighbor == v:
                return True
        return False

    def get_vertices_count(
        self,
    ):
        return len(self.adj_list)

    def get_neighbors(self, u):
        return [(neighbor, weight) for neighbor, weight in self.adj_list[u]]

    def get_adj_matrix(self):
        n = self.get_vertices_count()
        matrix = np.zeros((n, n))
        for u in range(n):
            for v, w in self.adj_list[u]:
                matrix[u, v] = w
        return matrix


# class IncedenceMatrixStorage(GraphStorage):
#     def __init__(self, inc_matrix):
#         self.inc_matrix = inc_matrix

#     # def add_edge(self, u, v, w = 1):
#     #     self.inc_matrix

#     def is_edge(self, u, v):
#         pass

#     def get_vertices_count(self):
#         return self.inc_matrix.shape()[0]

#     def get_neighbors(self, u):
#         neighbors = []
#         num_vertices, num_edges = self.inc_matrix.shape
#         for edge in range(num_edges):
#             if self.inc_matrix[u][edge] != 0:
#                 for v in range(num_vertices):
#                     if v != u and self.inc_matrix[v][edge] != 0:
#                         neighbors.append((v, self.inc_matrix[v][edge]))
#         return neighbors
