from typing import Any

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from factories import GraphFactory


def create_graph_from_ui(input_data, input_type, is_directed, is_weighted):
    """Оркестратор создания объекта графа из данных UI."""
    try:
        if input_type == "Матрица смежности":
            return GraphFactory.create_from_adj_matrix(
                input_data, is_weighted, is_directed
            )
        elif input_type == "Список смежности":
            return GraphFactory.create_from_adj_list(
                input_data, is_weighted, is_directed
            )
        elif input_type == "Матрица инцидентности":
            return GraphFactory.create_from_inc_matrix(
                input_data, is_weighted, is_directed
            )
    except ValueError as e:
        st.error(f"Ошибка в данных: {e}")
        st.stop()


def run_graph_input(force_directed=None, force_weighted=None):
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

    with st.expander(f"Редактирование графа ({input_type})", expanded=True):
        st.subheader("Конфигурация графа")
        edited_df = []
        # Матрица
        if input_type == "Матрица смежности":
            init_data = pd.DataFrame(np.zeros((n_vertices, n_vertices), dtype=int))
            edited_df = st.data_editor(init_data, key="matrix_editor")

        # Список смежности
        elif input_type == "Список смежности":
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

        else:
            max_edges = n_vertices * (n_vertices - 1) // 2 + n_vertices
            n_edges = st.number_input("Число ребер", 0, max_edges, n_vertices)

            init_inc_data = pd.DataFrame(
                np.zeros((n_vertices, n_edges), dtype=int),
                columns=[f"e{i}" for i in range(n_edges)],
                index=[f"V{i}" for i in range(n_vertices)],
            )
            edited_df = st.data_editor(
                init_inc_data, key="inc_editor", use_container_width=True
            )

    return create_graph_from_ui(edited_df, input_type, is_directed, is_weighted)


def draw_graph(
    graph, highlight_nodes=None, highlight_edges=None, node_colors: dict | None = None
):
    net = Network(height="400px", width="100%", directed=graph.is_directed())

    n_vertices = graph.get_vertices_count()
    palette = [
        "#e6194b",
        "#3cb44b",
        "#ffe119",
        "#4363d8",
        "#f58231",
        "#911eb4",
        "#46f0f0",
        "#f032e6",
        "#bcf60c",
        "#fabebe",
        "#008080",
        "#e6beff",
        "#9a6324",
        "#fffac8",
        "#800000",
        "#aaffc3",
        "#808000",
        "#ffd8b1",
        "#000075",
        "#808080",
    ]
    # Формирование вершин и раскраска
    for i in range(n_vertices):
        color = "#55ff00"  # Зеленый
        if node_colors is not None and i in node_colors:
            color_idx = node_colors[i]
            color = palette[color_idx % len(palette)]
        elif highlight_nodes and i in highlight_nodes:
            color = "#ff4b4b"  # Красный
        net.add_node(i, label=f"V{i}", color=color)

    # Формирование ребер
    for u in range(n_vertices):
        for v, weight in graph.get_neighbors(u):
            # Для неориентированного графа рисуем ребро один раз
            # Требует симметричности
            if not graph.is_directed() and u > v:
                continue

            edge_color = "#aaaaaa"  # Серый
            width = 1
            if highlight_edges and (u, v) in highlight_edges:
                edge_color = "#ff4b4b"  # Красный
                width = 3

            label = None
            if graph.is_weighted():
                label = str(weight)
            net.add_edge(u, v, color=edge_color, width=width, label=label)
    net.save_graph("graph.html")
    components.html(open("graph.html", "r").read(), height=450)


def show_qr():
    url = "http://godhunt.space:8501/"
    qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}"
    with st.sidebar:
        st.divider()
        st.image(qr_api_url, caption="Открыть приложение на телефоне")
