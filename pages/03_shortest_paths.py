import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Обходы")

# Ввод графа
matrix, adj_list, viz_matrix, processor = run_graph_input()


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
        result = processor.get_connected_components_count()
        st.success(f"Количество компоент: {result}")
        st.session_state["traversal_result"] = result

with tab2:
    st.subheader("Нахождение кратчайших путей от вершины")
    user_start_vertex = st.selectbox(
        label="Вершина",
        options=[v for v in range(len(viz_matrix))],
        # key=f"ms_{i}",
        key="vertex_dejikstra",
    )
    if st.button("Найти", key="button_dejikstra"):  # TODO
        shortest_paths = processor.get_shortest_paths_from(user_start_vertex)
        shortest_paths = {i: val for i, val in enumerate(shortest_paths)}
        cols = st.columns(len(shortest_paths))
        for i, val in shortest_paths.items():
            cols[i].metric(f"V{i}", val)

with tab3:
    st.subheader("Нахождение матрицы кратчайших путей")
    if st.button("Найти", key="button_matrix"):
        try:  # TODO
            user_input = user_input
            if processor.verify_components_count(user_input):
                st.balloons()
                st.success("Верно!")
            else:
                st.error(f"Неверно. Попробуйте еще раз")
        except ValueError:
            st.error("")  # !!

# --- Визуализация (универсальный блок) ---
st.divider()
st.subheader("Визуализация")

draw_graph(viz_matrix, is_weighted=True, is_directed=True)
