from abc import ABC, abstractmethod

import numpy as np


class GraphValidationError(ValueError):
    """Исключение для ошибок валидации структуры графа."""

    pass


class BaseInputValidator(ABC):
    def __init__(self, is_directed: bool, is_weighted: bool):
        self.is_directed = is_directed
        self.is_weighted = is_weighted

    @abstractmethod
    def validate(self, data):
        """
        Проверяет данные.
        Если данные некорректны, выбрасывает GraphValidationError.
        """
        pass


class AdjacencyMatrixValidator(BaseInputValidator):
    def validate(self, matrix):
        # Проверка на симметричность для неориентированного графа
        if not self.is_directed:
            if not np.allclose(matrix, matrix.T):
                raise GraphValidationError(
                    "Для неориентированного графа матрица должна быть симметричной относительно главной диагонали."
                )

        # Проверка на допустимые значения для невзвешенного графа
        if not self.is_weighted:
            if not np.all(np.isin(matrix, [0, 1])):
                raise GraphValidationError(
                    "Для невзвешенного графа разрешены только значения 0 или 1."
                )


class AdjacencyListValidator(BaseInputValidator):
    def validate(self, adj_list):
        n = len(adj_list)
        for u, neighbors in adj_list.items():
            seen_neighbors = set()
            for item in neighbors:
                v, weight = item
                # Проверка индексов вершин
                if not isinstance(v, int) or v < 0 or v >= n:
                    raise GraphValidationError(
                        f"Вершина {u}: недопустимый сосед {v}. Индексы должны быть в диапазоне [0, {n - 1}]."
                    )

                # Проверка типов весов
                if self.is_weighted and not isinstance(weight, (int, float)):
                    raise GraphValidationError(
                        f"Вершина {u}: вес до {v} должен быть числом."
                    )

                # Проверка на мультиребра (дубликаты)
                if v in seen_neighbors:
                    raise GraphValidationError(
                        f"Вершина {u} содержит дубликаты соседа {v}."
                    )
                seen_neighbors.add(v)

        # Проверка связности в обе стороны для неориентированного графа
        if not self.is_directed:
            for u, neighbors in adj_list.items():
                for item in neighbors:
                    v, w_uv = item
                    # Ищем обратное ребро v -> u
                    v_neighbors = adj_list.get(v, [])
                    found = False
                    for v_item in v_neighbors:
                        v_neighbor, w_vu = v_item

                        if v_neighbor == u:
                            if self.is_weighted and w_uv != w_vu:
                                raise GraphValidationError(
                                    f"Несоответствие весов: {u}->{v} (вес {w_uv}) и {v}->{u} (вес {w_vu})."
                                )
                            found = True
                            break

                    if not found:
                        raise GraphValidationError(
                            f"Отсутствует обратное ребро {v}->{u} для неориентированного графа."
                        )


class IncedencyMatrixValidator(BaseInputValidator):
    def validate(self, matrix):
        num_vertices, num_edges = matrix.shape

        for j in range(num_edges):
            col = matrix[:, j]
            idx = np.where(col != 0)[0]
            vals = col[idx]

            if len(idx) > 2:
                raise GraphValidationError(
                    f"Ребро {j}: инцидентно более чем двум вершинам."
                )

            if not self.is_weighted:
                if self.is_directed:
                    if len(idx) == 1:
                        if vals[0] != 2:
                            raise GraphValidationError(
                                f"Ребро {j}: петля в орграфе должна быть помечена 2."
                            )
                    else:
                        if not (1 in vals and -1 in vals):
                            raise GraphValidationError(
                                f"Ребро {j}: должно содержать 1 (выход) и -1 (вход)."
                            )
                else:
                    if len(idx) == 1:
                        if vals[0] != 2:
                            raise GraphValidationError(
                                f"Ребро {j}: петля должна быть помечена 2."
                            )
                    else:
                        if not np.all(vals == 1):
                            raise GraphValidationError(
                                f"Ребро {j}: обе вершины должны быть помечены 1."
                            )
            else:
                # Для взвешенных матриц инцидентности
                if self.is_directed:
                    if len(idx) == 2 and not np.isclose(vals[0], -vals[1]):
                        raise GraphValidationError(
                            f"Ребро {j}: веса должны быть w и -w для ориентированного ребра."
                        )
                else:
                    if len(idx) == 2 and not np.isclose(vals[0], vals[1]):
                        raise GraphValidationError(
                            f"Ребро {j}: веса должны совпадать для неориентированного ребра."
                        )
