import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Раскраска")

# Ввод графа
graph = run_graph_input(force_directed=False)

if "coloring" not in st.session_state:
    st.session_state["coloring"] = None

# Сброс раскраски в случае любого изменения самого графа
if graph:
    current_graph_bytes = graph.get_adj_matrix().tobytes()

    if (
        "last_graph_bytes" not in st.session_state
        or st.session_state["last_graph_bytes"] != current_graph_bytes
    ):
        st.session_state["coloring"] = None
        st.session_state["last_graph_bytes"] = current_graph_bytes


# Алгоритм
st.subheader("12. Раскраска графа")
if st.button("Найти"):
    result = Algos.get_coloring(graph)
    # st.success(f": {result}")
    st.session_state["coloring"] = result

# Визуализация
st.divider()
st.subheader("Визуализация")

if graph:
    draw_graph(graph, node_colors=st.session_state["coloring"])
