from abc import ABC, abstractmethod

from numpy._typing import NDArray


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

    def get_adj_matrix(self) -> NDArray:
        return self._storage.get_adj_matrix()


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
