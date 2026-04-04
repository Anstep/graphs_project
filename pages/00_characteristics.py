import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Характеристики графа")

# Ввод графа
matrix, adj_list, viz_matrix, processor = run_graph_input()

# Обработка и вывод
st.subheader("Характеристики графа")
if st.button("Рассчитать характеристики", type="primary"):
    st.session_state.calculated = True

if st.session_state.get("calculated"):
    st.divider()

    # 1.Степени вершин
    degrees = processor.get_vertex_degrees()

    st.subheader("Степени каждой вершины")
    # Вывод степеней в два ряда
    cols_deg = st.columns(len(degrees) if len(degrees) <= 10 else 10)
    for i, deg in enumerate(degrees):
        cols_deg[i % 10].metric(f"V{i}", deg)

    # st.divider()

    # 2. Число компонент и эйлеровость
    col1, col2, col3 = st.columns(3)

    with col1:
        comp_count = processor.get_connected_components_count()
        st.write("**Число компонент:**")
        st.info(f"{comp_count}")

    with col2:
        is_euler = processor.get_eulerian_status()
        st.write("**Эйлеровость:**")
        if is_euler:
            st.success(f"Эйлеров")
        else:
            st.warning(f"Не Эйлеров")

    with col3:
        is_bipartite = processor.get_bipartite_status()
        st.write("**Двудольность:**")
        if is_bipartite:
            st.success("Граф двудольный")
        else:
            st.warning("Не двудольный")


# --- Визуализация (универсальный блок) ---
st.divider()
st.subheader("Визуализация")


# def draw_graph(matrix, path_highlight=None):
#     net = Network(
#         height="400px",
#         width="100%",
#         bgcolor="#222222",
#         font_color="white",
#         directed=False,
#     )
#     for i in range(len(matrix)):
#         color = "#55ff00"
#         if path_highlight and i in path_highlight:
#             color = "#ff4b4b"  # Подсвечиваем пройденные вершины
#         net.add_node(i, label=f"V{i}", color=color)

#     rows, cols = np.where(np.triu(np.array(matrix)) > 0)
#     for u, v in zip(rows, cols):
#         net.add_edge(int(u), int(v), color="#aaaaaa")

#     net.save_graph("graph.html")
#     with open("graph.html", "r", encoding="utf-8") as f:
#         components.html(f.read(), height=450)


draw_graph(viz_matrix)
