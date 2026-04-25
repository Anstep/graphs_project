import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="MST")

# Ввод графа
graph = run_graph_input(force_directed=False, force_weighted=True)

# Algo selection
tab1 = st.tabs(
    [
        "7. Построение минимального остовного дерева",
    ]
)

# Обработка
st.subheader("Построение минимального остовного дерева")
# Код алгоритма и визуализация для задачи 1
if st.button("Построить"):
    res = Algos.mst_kruskal(graph)
    res = [tup[:2] for tup in res]
    st.session_state["highlight_edges"] = res
    st.success("Дерево построено")

# --- Визуализация (универсальный блок) ---
st.divider()
st.subheader("Визуализация")

# Инициализация состояний для визуализации
if "highlight_edges" not in st.session_state:
    st.session_state["highlight_edges"] = None

draw_graph(
    graph,
    highlight_edges=st.session_state.get("highlight_edges"),
)
