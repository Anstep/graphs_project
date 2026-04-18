from abc import ABC, abstractmethod

import numpy as np


class OperationResult:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error
        self.is_success = error is None


class BaseInputValidator(ABC):
    def __init__(self, is_directed, is_weighted):
        self.is_directed = is_directed
        self.is_weighted = is_weighted

    @abstractmethod
    def validate(self, data):
        pass


class AdjacencyMatrixValidator(BaseInputValidator):
    def validate(self, matrix):
        if not self.is_directed:
            if not (matrix == matrix.T).all():
                return OperationResult(
                    error="Для неориентированного графа матрица должна быть симметричной относительно главной диагонали."
                )

        if not self.is_weighted:
            if not np.all(np.isin(matrix, [0, 1])):
                return OperationResult(
                    error="Для невзвешенного графа разрешено только 0 или 1"
                )

        return OperationResult(data=True)


class AdjacencyListValidator(BaseInputValidator):
    def validate(self, adj_list):
        n = len(adj_list)
        for u, neighbors in adj_list.items():
            seen_neighbors = set()
            for item in neighbors:
                v, weight = (item[0], item[1]) if self.is_weighted else (item, 1)

                if not isinstance(v, int) or v < 0 or v >= n:
                    return OperationResult(
                        error=f"Вершина {u}: недопустимый сосед {v}. Индексы должны быть в диапазоне [0, {n - 1}]."
                    )

                if self.is_weighted and not isinstance(weight, (int, float)):
                    return OperationResult(
                        error=f"Вершина {u}: вес до {v} должен быть числом."
                    )

                if v in seen_neighbors:
                    return OperationResult(
                        error=f"Вершина {u} содержит дубликаты соседа {v}."
                    )
                seen_neighbors.add(v)

        if not self.is_directed:
            for u, neighbors in adj_list.items():
                for item in neighbors:
                    v, w_uv = (item[0], item[1]) if self.is_weighted else (item, 1)
                    found = False
                    v_neighbors = adj_list.get(v, [])
                    for v_item in v_neighbors:
                        v_neighbor, w_vu = (
                            (v_item[0], v_item[1]) if self.is_weighted else (v_item, 1)
                        )
                        if v_neighbor == u:
                            if self.is_weighted and w_uv != w_vu:
                                return OperationResult(
                                    error=f"Несоответствие весов: {u}->{v} ({w_uv}) и {v}->{u} ({w_vu})."
                                )
                            found = True
                            break

                    if not found:
                        return OperationResult(
                            error=f"Отсутствует обратное ребро {v}->{u} для неориентированного графа."
                        )
        return OperationResult(data=True)


class IncedencyMatrixValidator(BaseInputValidator):
    def validate(self, matrix):
        for j in range(matrix.shape[1]):
            col = matrix[:, j]
            idx = np.where(col != 0)[0]
            vals = col[idx]

            if len(idx) == 0:
                continue

            if len(idx) > 2:
                return OperationResult(
                    error=f"Ребро {j}: инцидентно более чем двум вершинам ({len(idx)})."
                )

            if not self.is_weighted:
                if self.is_directed:
                    if len(idx) == 1:
                        if vals[0] != 2:
                            return OperationResult(
                                error=f"Ребро {j}: петля в орграфе должна быть помечена 2."
                            )
                    else:
                        if not (1 in vals and -1 in vals):
                            return OperationResult(
                                error=f"Ребро {j}: должно содержать 1 (выход) и -1 (вход)."
                            )
                else:
                    if len(idx) == 1:
                        if vals[0] != 2:
                            return OperationResult(
                                error=f"Ребро {j}: петля должна быть помечена 2."
                            )
                    else:
                        if not np.all(vals == 1):
                            return OperationResult(
                                error=f"Ребро {j}: обе вершины должны быть помечены 1."
                            )
            else:
                if self.is_directed:
                    if len(idx) == 2 and vals[0] != -vals[1]:
                        return OperationResult(
                            error=f"Ребро {j}: веса должны быть w и -w для ориентированного ребра."
                        )
                else:
                    if len(idx) == 2 and vals[0] != vals[1]:
                        return OperationResult(
                            error=f"Ребро {j}: веса должны совпадать для неориентированного ребра."
                        )
        return OperationResult(data=True)
