from core.graphs import DirectedGraph, UndirectedGraph
from core.parsers import InputParsers
from core.storage import AdjacencyListStorage, AdjacencyMatrixStorage
from core.validators import (
    AdjacencyListValidator,
    AdjacencyMatrixValidator,
    IncedencyMatrixValidator,
)


class GraphFactory:
    @staticmethod
    def create_from_adj_matrix(input, is_weighted, is_directed):
        data = InputParsers.parse_adj_matrix(input, is_directed, is_weighted)
        validator = AdjacencyMatrixValidator(is_directed, is_weighted)
        validator.validate(data)
        storage = AdjacencyMatrixStorage(data)

        if is_directed:
            return DirectedGraph(storage, is_weighted=is_weighted)
        return UndirectedGraph(storage, is_weighted=is_weighted)

    @staticmethod
    def create_from_adj_list(input: dict, is_weighted, is_directed):
        data = InputParsers.parse_adj_list(input, is_directed, is_weighted)
        validator = AdjacencyListValidator(is_directed, is_weighted)
        validator.validate(data)
        storage = AdjacencyListStorage(data)

        if is_directed:
            return DirectedGraph(storage, is_weighted=is_weighted)
        return UndirectedGraph(storage, is_weighted=is_weighted)

    @staticmethod
    def create_from_inc_matrix(input, is_weighted, is_directed):
        data = InputParsers.parse_inc_matrix(input, is_directed, is_weighted)

        adj_matrix = InputParsers.inc_matrix_to_adj_matrix(
            data, is_directed, is_weighted
        )
        validator = IncedencyMatrixValidator(is_directed, is_weighted)
        validator.validate(data)

        storage = AdjacencyMatrixStorage(adj_matrix)

        if is_directed:
            return DirectedGraph(storage, is_weighted=is_weighted)
        return UndirectedGraph(storage, is_weighted=is_weighted)

    @staticmethod
    def create_from_edges(edges, n_vertices):
        """
        Создание графа из ребер для задания 11.
        """
        data = InputParsers.parse_edges_list(edges, n_vertices)
        storage = AdjacencyListStorage(data)

        return UndirectedGraph(storage, is_weighted=False)
