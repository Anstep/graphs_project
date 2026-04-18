from abc import ABC, abstractmethod


class GraphStorage(ABC):
    # @abstractmethod
    # def add_edge(self, u, v, w):
    #     pass

    @abstractmethod
    def is_edge(self, u, v):
        pass

    @abstractmethod
    def get_vertices_count(self):
        pass

    @abstractmethod
    def get_neighbors(self, u):
        pass


class AdjacencyMatrixStorage(GraphStorage):
    def __init__(self, matrix):
        self.adj_matrix = matrix

    # def add_edge(self, u, v, w = 1):
    #     self.adj_matrix[u][v] = w

    def is_edge(self, u, v):
        return True if self.adj_matrix[u][v] else False

    def get_vertices_count(self):
        return self.adj_matrix.shape[0]

    # TODO переписать с numpy
    def get_neighbors(self, u):
        return [
            (v, self.adj_matrix[u][v])
            for v in range(self.get_vertices_count())
            if self.adj_matrix[u][v] != 0
        ]


class AdjacencyListStorage(GraphStorage):
    def __init__(self, adj_list):
        self.adj_list = adj_list

    # def add_edge(self, u, v, w):
    #     self.adj_list[u].append((v, w))

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
