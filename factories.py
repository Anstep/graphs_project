from core.graphs import DirectedGraph, UndirectedGraph
from core.parsers import InputParsers
from core.storage import *
from core.validators import (
    AdjacencyListValidator,
    AdjacencyMatrixValidator,
    IncedencyMatrixValidator,
)


class GraphFactory:
    @staticmethod
    def create_from_adj_matrix(input, is_weighted, is_directed):
        """
        Выбрасывает ислключение?
        """
        data = InputParsers.parse_adj_matrix(input, is_directed, is_weighted)

        # validator = AdjacencyMatrixValidator(is_directed, is_weighted)
        # validator.validate(data)

        storage = AdjacencyMatrixStorage(data)

        return DirectedGraph(storage) if is_directed else UndirectedGraph(storage)

    @staticmethod
    def create_from_adj_list(input: dict, is_weighted, is_directed):
        """
        Выбрасывает ислключение?
        """
        data = InputParsers.parse_adj_list(input, is_directed, is_weighted)

        # validator = AdjacencyListValidator(is_directed, is_weighted)
        # validator.validate(data)

        storage = AdjacencyListStorage(data)

        return DirectedGraph(storage) if is_directed else UndirectedGraph(storage)

    @staticmethod
    def create_from_inc_matrix(input, is_weighted, is_directed):
        """
        Выбрасывает ислключение?
        """
        data = InputParsers.parse_inc_matrix(input, is_directed, is_weighted)

        # validator = IncedencyMatrixValidator(is_directed, is_weighted)
        # validator.validate(data)

        adj_matrix = InputParsers.inc_matrix_to_adj_matrix(
            data, is_directed, is_weighted
        )
        storage = AdjacencyMatrixStorage(adj_matrix)

        return DirectedGraph(storage) if is_directed else UndirectedGraph(storage)
