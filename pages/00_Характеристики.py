import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Характеристики графа")

# Ввод графа
graph = run_graph_input(force_directed=False, force_weighted=False)

# Обработка и вывод
st.subheader("Характеристики графа")

if st.button("Рассчитать характеристики", type="primary"):
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
        is_euler = Algos.is_eulerian(graph)
        st.write("**Эйлеровость:**")
        if is_euler:
            st.success(f"Эйлеров")
        else:
            st.warning(f"Не Эйлеров")

    with col3:
        bipartite_status = Algos.get_bipartite_status(graph)
        st.write("**Двудольность:**")
        if bipartite_status == "none":
            st.warning("Не двудольный")
        elif bipartite_status == "simple":
            st.success("Обычный двудольный")
        else:
            st.success("Полный двудольный")


# Визуализация
st.divider()
st.subheader("Визуализация")

draw_graph(graph)
