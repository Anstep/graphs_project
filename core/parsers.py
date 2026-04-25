import numpy as np


class InputParsers:
    @staticmethod
    def parse_adj_matrix(df, is_directed, is_weighted):
        return df.to_numpy()

    @staticmethod
    def parse_adj_list(df, is_directed, is_weighted) -> dict:
        adj_list = {}
        for i, row in df.iterrows():
            line = str(row.iloc[0]).strip()
            neighbors = []
            if line:
                # Очистка от возможных скобок и разделение
                line = (
                    line.replace("(", "")
                    .replace(")", "")
                    .replace("[", "")
                    .replace("]", "")
                )
                for part in line.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    if is_weighted:
                        if ":" not in part:
                            raise ValueError(
                                f"Вершина {i}: ожидался формат v:w для '{part}'"
                            )
                        v_str, w_str = part.split(":")
                        neighbors.append((int(v_str.strip()), float(w_str.strip())))
                    else:
                        neighbors.append((int(part), 1))
            adj_list[i] = neighbors
        return adj_list

    @staticmethod
    def parse_inc_matrix(df, is_directed, is_weighted):
        return df.to_numpy()

    @staticmethod
    def inc_matrix_to_adj_matrix(matrix, is_directed, is_weighted):
        num_vertices = matrix.shape[0]
        num_edges = matrix.shape[1]
        adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
        for j in range(num_edges):
            # получаем соответствующий столбец
            col = matrix[:, j]
            # крайне удобная функция numpy
            idxs = np.where(col != 0)[0]

            if len(idxs) != 2:
                continue

            if is_directed:
                input = np.where(col > 0)[0]
                out = np.where(col < 0)[0]
                u, v = input[0], out[0]
                adj_matrix[u][v] = col[u]
            else:
                u, v = idxs[0], idxs[1]
                w = col[u]
                adj_matrix[u][v] = w
                adj_matrix[v][u] = w
        return adj_matrix

    @staticmethod
    def parse_edges_list(edges, n_vertices) -> dict:
        adj_list = {i: [] for i in range(n_vertices)}
        for edge in edges:
            u, v = edge
            w = 1

            adj_list[u].append((v, w))
            adj_list[v].append((u, w))
        return adj_list
