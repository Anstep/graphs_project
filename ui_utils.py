import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from graph import Graph


def run_graph_input():
    with st.sidebar:
        st.subheader("Конфигурация")
        n_vertices = st.number_input("Число вершин", 1, 20, 5)
        input_type = st.radio(
            "Метод ввода",
            ["Матрица смежности", "Список смежности", "Матрица инцидентности"],
        )

    matrix = None
    adj_list = None

    with st.expander(f"Редактирование графа ({input_type})", expanded=True):
        st.subheader("Конфигурация графа")

        # Генерация матрицы
        if input_type == "Матрица смежности":
            init_data = pd.DataFrame(np.zeros((n_vertices, n_vertices), dtype=int))
            edited_df = st.data_editor(init_data, key="matrix_editor")
            matrix = edited_df.to_numpy().tolist()
            processor = Graph(n_vertices, adj_matrix=matrix)
            viz_matrix = matrix

        elif input_type == "Список смежности":
            adj_list = {}

            cols = st.columns(3)
            for i in range(n_vertices):
                col_idx = i % 3
                selected_neighbors = cols[col_idx].multiselect(
                    label=f"Вершина {i} соединена с:",
                    options=[v for v in range(n_vertices) if v != i],
                    key=f"ms_{i}",
                    default=[],
                )
                adj_list[i] = selected_neighbors

            processor = Graph(n_vertices, adj_list=adj_list)
            viz_matrix = [[0] * n_vertices for _ in range(n_vertices)]
            for u, neighbors in adj_list.items():
                for v in neighbors:
                    viz_matrix[u][v] = 1

        else:
            n_edges = st.number_input(
                "Число ребер", 0, n_vertices * (n_vertices - 1) // 2, n_vertices
            )

            init_inc_data = pd.DataFrame(
                np.zeros((n_vertices, n_edges), dtype=int),
                columns=[f"r{i}" for i in range(n_edges)],
                index=[f"V{i}" for i in range(n_vertices)],
            )
            edited_inc_df = st.data_editor(
                init_inc_data, key="inc_editor", use_container_width=True
            )
            inc_matrix = edited_inc_df.to_numpy()

            # 2. Инициализация выходных структур
            adj_dict = {i: [] for i in range(n_vertices)}
            viz_matrix = [[0] * n_vertices for _ in range(n_vertices)]

            # 3. Проход по ребрам (столбцам) для формирования связей
            for j in range(n_edges):
                # Находим индексы всех ненулевых строк в текущем столбце j
                nodes = np.where(inc_matrix[:, j] > 0)[0]

                # Если в столбце ровно две единицы — это ребро между u и v
                if len(nodes) == 2:
                    u, v = int(nodes[0]), int(nodes[1])

                    # Заполнение словаря (adj_list)
                    if v not in adj_dict[u]:
                        adj_dict[u].append(v)
                    if u not in adj_dict[v]:
                        adj_dict[v].append(u)

                    # Заполнение матрицы визуализации (viz_matrix)
                    viz_matrix[u][v] = 1
                    viz_matrix[v][u] = 1

                # Обработка петли (одна единица со значением 2 или просто одна единица)
                elif len(nodes) == 1:
                    u = int(nodes[0])
                    viz_matrix[u][u] = 1
                    if u not in adj_dict[u]:
                        adj_dict[u].append(u)
            processor = Graph(n_vertices, adj_list=adj_dict)
        # if input_type == "Список смежности" and adj_list is not None:
        #     viz_matrix = [[0] * n_vertices for _ in range(n_vertices)]
        #     for u, neighbors in adj_list.items():
        #         for v in neighbors:
        #             viz_matrix[u][v] = 1
        # else:
        #     viz_matrix = matrix

    return matrix, adj_list, viz_matrix, processor


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

    # Добавление узлов
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

        # Подсветка конкретных ребер (например, для MST)
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
