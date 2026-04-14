from typing import Any

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from graph import Graph


def validate_adj_matrix(
    matrix: np.ndarray, is_directed=False, is_weighted=False
) -> str | None:
    """
    Валидация матрицы смежности.
    Проверяет:
    - Симметричность относительно главной диагонали (для неориентированных)
    - Допустимые значения: {0, 1} для невзвешенных, >=0 для взвешенных
    - Отсутствие петель на главной диагонали (если требуется)
    Возвращает текст ошибки или None.
    """
    # 1. Проверка на симметричность
    if not is_directed:
        if not (matrix == matrix.T).all():
            return "Для неориентированного графа матрица должна быть симметричной относительно главной диагонали."

    # 2. Проверка на допустимые значения (веса)
    if not is_weighted:
        if not np.all(np.isin(matrix, [0, 1])):
            return "В невзвешенном графе допустимы только значения 0 и 1."

    # 3. Проверка на отсутсвтие петель
    #
    return None


def validate_adj_list(
    adj_list: dict[int, list[int | tuple[int, float]]],
    is_directed=False,
    is_weighted=False,
) -> str | None:
    """
    Валидация списка смежности.
    Проверяет:
    - Диапазон индексов соседей
    - Симметричность связей (u в списке v <=> v в списке u) для неориентированных
    - Формат и знак весов для взвешенных графов
    - Отсутствие дубликатов соседей
    Возвращает текст ошибки или None.
    """
    n = len(adj_list)
    for u, neighbors in adj_list.items():
        seen_neighbors = set()
        for item in neighbors:
            v, weight = (item[0], item[1]) if is_weighted else (item, 1)

            if not isinstance(v, int) or v < 0 or v >= n:
                return f"Вершина {u}: недопустимый сосед {v}. Индексы должны быть в диапазоне [0, {n - 1}]."

            if is_weighted and not isinstance(weight, (int, float)):
                return f"Вершина {u}: вес до {v} должен быть числом."

            if v in seen_neighbors:
                return f"Вершина {u} содержит дубликаты соседа {v}."
            seen_neighbors.add(v)

    if not is_directed:
        for u, neighbors in adj_list.items():
            for item in neighbors:
                v, w_uv = (item[0], item[1]) if is_weighted else (item, 1)
                # Поиск обратного ребра v -> u
                found = False
                v_neighbors = adj_list.get(v, [])
                for v_item in v_neighbors:
                    v_neighbor, w_vu = (
                        (v_item[0], v_item[1]) if is_weighted else (v_item, 1)
                    )
                    if v_neighbor == u:
                        if is_weighted and w_uv != w_vu:
                            return f"Несоответствие весов: {u}->{v} ({w_uv}) и {v}->{u} ({w_vu})."
                        found = True
                        break

                if not found:
                    return f"Отсутствует обратное ребро {v}->{u} для неориентированного графа."
    return None

    # 3. Проверка на отсутствие петель (если нужно, можно добавить опционально)
    # for u, neighbors in adj_list.items():
    #     if u in neighbors:
    #         return f"Обнаружена петля у вершины {u}."


def validate_inc_matrix(
    matrix: np.ndarray,
    is_directed: bool,
    is_weighted: bool,
    n_edges: int,
) -> str | None:
    """
    Валидация матрицы инцидентности.
    Проверяет:
    - Сумму элементов столбцов (2 для ребра, 1 для петли, 0 для изоляции)
    - Для орграфов: наличие ровно одной 1 и одной -1 в столбце (или 2 для петли)
    - Допустимые значения ячеек
    Возвращает текст ошибки или None.
    """
    for j in range(n_edges):
        col = matrix[:, j]
        idx = np.where(col != 0)[0]
        vals = col[idx]

        if len(idx) == 0:
            continue

        if len(idx) > 2:
            return f"Ребро {j}: инцидентно более чем двум вершинам ({len(idx)})."

        if not is_weighted:
            if is_directed:
                if len(idx) == 1:
                    if vals[0] != 2:
                        return f"Ребро {j}: петля в орграфе должна быть помечена 2."
                else:  # len(idx) == 2
                    if not (1 in vals and -1 in vals):
                        return f"Ребро {j}: должно содержать 1 (выход) и -1 (вход)."
            else:
                if len(idx) == 1:
                    if vals[0] != 2:
                        return f"Ребро {j}: петля должна быть помечена 2."
                else:  # len(idx) == 2
                    if not np.all(vals == 1):
                        return f"Ребро {j}: обе вершины должны быть помечены 1."
        else:
            if is_directed:
                if len(idx) == 2 and vals[0] != -vals[1]:
                    return f"Ребро {j}: веса должны быть w и -w для ориентированного ребра."
            else:
                if len(idx) == 2 and vals[0] != vals[1]:
                    return f"Ребро {j}: веса должны совпадать для неориентированного ребра."
    return None


def validate_weighted_graph_constraints(
    matrix: np.ndarray, is_directed: bool, algorithm: str, processor: Any = None
) -> str | None:
    """
    Дополнительная валидация для взвешенных графов.
    Проверяет:
    - Отсутствие отрицательных весов (критично для Дейкстры)
    - Связность графа (критично для MST)
    - Корректность весовых меток
    Возвращает текст ошибки или None.
    """
    if algorithm == "Dijkstra":
        if np.any(matrix < 0):
            return "Ошибка: Алгоритм Дейкстры не поддерживает отрицательные веса ребер."

    if algorithm == "MST":
        # if is_directed:
        #     return "Ошибка: Алгоритм построения MST (Прима/Краскала) предназначен для неориентированных графов."
        if processor and processor.get_connected_components_count() > 1:
            return "Предупреждение: Граф несвязен. Алгоритм построит минимальный остовный лес (набор деревьев для каждой компоненты)."

    if algorithm == "Floyd":
        pass


def run_graph_input(
    force_directed: bool | None = None, force_weighted: bool | None = None
):
    with st.sidebar:
        st.subheader("Конфигурация")
        n_vertices = st.number_input("Число вершин", 1, 20, 5)
        is_directed = (
            force_directed
            if force_directed is not None
            else st.checkbox("Ориентированный граф")
        )
        is_weighted = (
            force_weighted
            if force_weighted is not None
            else st.checkbox("Взвешенный граф")
        )
        input_type = st.radio(
            "Метод ввода",
            ["Матрица смежности", "Список смежности", "Матрица инцидентности"],
        )

    matrix = None
    adj_list = None

    with st.expander(f"Редактирование графа ({input_type})", expanded=True):
        st.subheader("Конфигурация графа")

        # Матрица
        if input_type == "Матрица смежности":
            init_data = pd.DataFrame(np.zeros((n_vertices, n_vertices), dtype=int))
            edited_df = st.data_editor(init_data, key="matrix_editor")
            matrix = edited_df.to_numpy()
            error = validate_adj_matrix(matrix, is_directed, is_weighted)
            if error:
                st.error(error)
                st.stop()
            processor = Graph(n_vertices, adj_matrix=matrix)
            viz_matrix = matrix

        # Список смежности
        elif input_type == "Список смежности":
            adj_list = {}
            col_name = (
                "Соседи и веса (v:w, ...)" if is_weighted else "Соседи (через запятую)"
            )
            init_df = pd.DataFrame(
                {col_name: [""] * n_vertices},
                index=[i for i in range(n_vertices)],
            )

            edited_df = st.data_editor(
                init_df, key="adj_list_editor", use_container_width=True
            )

            try:
                for idx, row in edited_df.iterrows():
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
                                        f"Вершина {idx}: ожидался формат v:w для '{part}'"
                                    )
                                v_str, w_str = part.split(":", 1)
                                neighbors.append(
                                    (int(v_str.strip()), float(w_str.strip()))
                                )
                            else:
                                neighbors.append(int(part))
                    adj_list[idx] = neighbors

                error = validate_adj_list(adj_list, is_directed, is_weighted)
                if error:
                    st.error(error)
                    st.stop()

                processor = Graph(n_vertices, adj_list=adj_list)
                viz_matrix = np.zeros(
                    (n_vertices, n_vertices), dtype=float if is_weighted else int
                )
                for u, neighbors in adj_list.items():
                    for item in neighbors:
                        v, w = (item[0], item[1]) if is_weighted else (item, 1)
                        viz_matrix[u][v] = w

            except ValueError as e:
                st.error(f"Ошибка формата: {e}")
                st.stop()

        # Матрица инцидентности
        else:
            max_edges = n_vertices * (n_vertices - 1) // 2 + n_vertices
            n_edges = st.number_input("Число ребер", 0, max_edges, n_vertices)

            init_inc_data = pd.DataFrame(
                np.zeros((n_vertices, n_edges), dtype=int),
                columns=[f"e{i}" for i in range(n_edges)],
                index=[f"V{i}" for i in range(n_vertices)],
            )
            edited_inc_df = st.data_editor(
                init_inc_data, key="inc_editor", use_container_width=True
            )
            inc_matrix = edited_inc_df.to_numpy()

            error = validate_inc_matrix(
                inc_matrix, is_directed, is_weighted, n_vertices
            )
            if error:
                st.error(error)
                st.stop()

            viz_matrix = np.zeros((n_vertices, n_vertices))

            for j in range(n_edges):
                col = inc_matrix[:, j]
                nodes = np.where(col != 0)[0]

                if len(nodes) == 2:
                    u, v = int(nodes[0]), int(nodes[1])
                    if is_directed:
                        start = u if col[u] > 0 else v
                        end = v if col[u] > 0 else u
                        viz_matrix[start][end] = col[start]
                    else:
                        viz_matrix[u][v] = col[u]
                        viz_matrix[v][u] = col[u]
                elif len(nodes) == 1:
                    u = int(nodes[0])
                    # Для петли в невзвешенном графе ставим 1, во взвешенном — значение из матрицы
                    viz_matrix[u][u] = col[u] if is_weighted else 1

            processor = Graph(n_vertices, adj_matrix=viz_matrix)
    return viz_matrix, is_directed, processor


def draw_graph(
    matrix,
    node_colors=None,  # Словарь {индекс: цвет} для раскраски
    highlight_nodes=None,  # Список индексов для обходов
    highlight_edges=None,  # Список кортежей [(u, v), ...] для MST/путей
    is_weighted=False,  # Нужно ли рисовать веса
    is_directed=False,  # Направленный ли граф
):

    net = Network(
        height="400px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=is_directed,
    )

    # Добавление вершин
    for i in range(len(matrix)):
        color = "#55ff00"  # Стандартный цвет
        if node_colors and i in node_colors:
            color = node_colors[i]
        elif highlight_nodes and i in highlight_nodes:
            color = "#ff4b4b"  # Цвет подсветки (красный)

        net.add_node(i, label=f"V{i}", color=color)

    # Добавление ребер
    matrix_np = np.array(matrix)
    # Если граф неориентированный, берем только верхний треугольник, чтобы не дублировать ребра
    rows, cols = np.where(matrix_np > 0)

    for u, v in zip(rows, cols):
        if not is_directed and u > v:
            continue

        weight = matrix_np[u][v]
        edge_color = "#aaaaaa"
        width = 1

        # Подсветка конкретных ребер
        if highlight_edges and (
            (u, v) in highlight_edges or (not is_directed and (v, u) in highlight_edges)
        ):
            edge_color = "#ff4b4b"
            width = 3

        label = str(weight) if is_weighted else None
        net.add_edge(int(u), int(v), color=edge_color, width=width, label=label)

    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=450)
