import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Раскраска")

# Ввод графа
graph = run_graph_input(force_directed=False)

st.subheader("12. Раскраска графа")
if st.button("Найти"):
    result = Algos.get_coloring(graph)
    st.success(f": {result}")
    st.session_state["coloring"] = result

# Визуализация
st.divider()
st.subheader("Визуализация ")

if "coloring" not in st.session_state:
    st.session_state["coloring"] = None

if graph:
    draw_graph(graph, node_colors=st.session_state["coloring"])
    print(st.session_state["coloring"])
