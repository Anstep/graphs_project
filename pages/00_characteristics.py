import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Характеристики графа")

# Ввод графа
graph = run_graph_input()

# Обработка и вывод
st.subheader("Характеристики графа")
if st.button("Рассчитать характеристики", type="primary"):
    st.session_state.calculated = True

if st.session_state.get("calculated"):
    st.divider()

    # 1.Степени вершин
    degrees = Algos.get_vertices_degrees(graph)

    st.subheader("Степени каждой вершины")
    # Вывод степеней в два ряда
    cols_deg = st.columns(len(degrees) if len(degrees) <= 10 else 10)
    for i, deg in enumerate(degrees):
        cols_deg[i % 10].metric(f"V{i}", deg)

    # st.divider()

    # 2. Число компонент и эйлеровость
    col1, col2, col3 = st.columns(3)

    with col1:
        comp_count = Algos.get_connected_components_count(graph)
        st.write("**Число компонент:**")
        st.info(f"{comp_count}")

    with col2:
        is_euler = Algos.get_eulerian_status(graph)
        st.write("**Эйлеровость:**")
        if is_euler:
            st.success(f"Эйлеров")
        else:
            st.warning(f"Не Эйлеров")

    with col3:
        is_bipartite = Algos.get_bipartite_status(graph)
        st.write("**Двудольность:**")
        if is_bipartite:
            st.success("Граф двудольный")
        else:
            st.warning("Не двудольный")


# --- Визуализация (универсальный блок) ---
st.divider()
st.subheader("Визуализация")

draw_graph(graph)
