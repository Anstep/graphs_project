import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from ui_utils import draw_graph, run_graph_input, validate_weighted_graph_constraints

# Настройка страницы
st.set_page_config(layout="wide", page_title="Обходы")

# Ввод графа
matrix, adj_list, viz_matrix, is_directed, processor = run_graph_input(
    force_weighted=True
)

# Algo selection
tab1, tab2, tab3 = st.tabs(
    [
        "7. Построение минимального остовного дерева",
        "8. Нахождение кратчайших путей от вершины",
        "9. Нахождение матрицы кратчайших путей",
    ]
)

# Обработка
with tab1:
    st.subheader("Построение минимального остовного дерева")
    # Код алгоритма и визуализация для задачи 1
    if st.button("Построить"):
        # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
        error = validate_weighted_graph_constraints(
            viz_matrix, is_directed, "MST", processor
        )
        if error:
            if "Ошибка" in error:
                st.error(error)
                st.stop()
            else:
                st.warning(error)
        st.session_state["highlight_edges"] = processor.get_minimal_spanning_tree()
        st.success("Дерево построено")


with tab2:
    st.subheader("Нахождение кратчайших путей от вершины")
    user_start_vertex = st.selectbox(
        label="Вершина",
        options=[v for v in range(len(viz_matrix))],
        key="vertex_dijkstra",
    )
    if st.button("Найти", key="button_dejikstra"):  # TODO
        error = validate_weighted_graph_constraints(viz_matrix, is_directed, "Dijkstra")
        if error:
            st.error(error)
            st.stop()

        st.session_state["highlight_edges"] = None
        shortest_paths = processor.get_shortest_paths_from(user_start_vertex)
        cols = st.columns(len(shortest_paths))
        for i, val in enumerate(shortest_paths):
            cols[i].metric(f"V{i}", "∞" if val == -1 else val)

with tab3:
    st.subheader("Нахождение матрицы кратчайших путей")
    if st.button("Найти", key="button_matrix"):
        st.session_state["highlight_edges"] = None
        dist_matrix = processor.get_matrix_shortest_paths()
        st.dataframe(pd.DataFrame(dist_matrix))

# --- Визуализация (универсальный блок) ---
st.divider()
st.subheader("Визуализация")

# Инициализация состояний для визуализации
if "highlight_edges" not in st.session_state:
    st.session_state["highlight_edges"] = None

draw_graph(
    viz_matrix,
    highlight_edges=st.session_state.get("highlight_edges"),
    is_weighted=True,
    is_directed=is_directed,
)
