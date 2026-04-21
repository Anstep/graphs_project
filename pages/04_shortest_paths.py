import pandas as pd
import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Кратчайшие пути")

# Ввод графа
graph = run_graph_input(force_weighted=True)

# Algo selection
tab1, tab2 = st.tabs(
    [
        "8. Нахождение кратчайших путей от вершины",
        "9. Нахождение матрицы кратчайших путей",
    ]
)

with tab1:
    st.subheader("Нахождение кратчайших путей от вершины")
    user_start_vertex = st.selectbox(
        label="Вершина",
        options=[v for v in range(graph.get_vertices_count())],
        key="vertex_dijkstra",
    )
    if st.button("Найти", key="button_dejikstra"):  # TODO
        # error = validate_weighted_graph_constraints(viz_matrix, is_directed, "Dijkstra")
        # if error:
        #     st.error(error)
        #     st.stop()

        st.session_state["highlight_edges"] = None
        res = Algos.get_shortest_paths_from(graph, user_start_vertex)
        if not res:
            st.error("Ошибка при расчете (возможно, отрицательные веса)")
            st.stop()
        shortest_paths, pred = res
        cols = st.columns(len(shortest_paths))
        for i, val in enumerate(shortest_paths):
            cols[i].metric(f"V{i}", "∞" if val == -1 else val)
        mode = st.radio(
            "Режим визуализации:", ["Весь остов (дерево)", "Конкретный путь"]
        )
        if mode == "Весь остов (дерево)":
            st.session_state["highlight_edges"] = Algos.get_shortest_edges_dijkstra(
                pred
            )
        # else:
        #     target_v = st.selectbox("До вершины:", range(graph.get_vertices_count()))
        #     if shortest_paths[target_v] != -1:
        #         path = Algos.reconstruct_path_dijkstra(pred, target_v)
        #         path_edges = []
        #         for i in range(len(path) - 1):
        #             path_edges.append(tuple(sorted((path[i], path[i + 1]))))
        #         st.session_state["highlight_edges"] = path_edges

with tab2:
    st.subheader("Нахождение матрицы кратчайших путей")
    if st.button("Найти", key="button_matrix"):
        st.session_state["highlight_edges"] = None
        dist_matrix = Algos.get_matrix_shortest_paths(graph)
        st.dataframe(pd.DataFrame(dist_matrix))

# Визуализация
st.divider()
st.subheader("Визуализация")

# Инициализация состояний для визуализации
if "highlight_edges" not in st.session_state:
    st.session_state["highlight_edges"] = None

draw_graph(
    graph,
    highlight_edges=st.session_state.get("highlight_edges"),
)
