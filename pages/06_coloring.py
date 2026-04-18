import streamlit as st

from core.algorithms import Algos
from ui_utils import run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Раскраска")

# Ввод графа
graph = run_graph_input(force_directed=False)


st.subheader("12. Раскраска графа")
# Код алгоритма и визуализация для задачи 1
if st.button("Найти"):  # TODO
    # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
    result = Algos.get_connected_components_count(graph)
    st.success(f": {result}")
    st.session_state["coloring"] = result

# Визуализация
st.divider()
st.subheader("Визуализация ")

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
#             color = "#ff4b4b"
#         net.add_node(i, label=f"V{i}", color=color)

#     rows, cols = np.where(np.triu(np.array(matrix)) > 0)
#     for u, v in zip(rows, cols):
#         net.add_edge(int(u), int(v), color="#aaaaaa")

#     net.save_graph("graph.html")
#     with open("graph.html", "r", encoding="utf-8") as f:
#         components.html(f.read(), height=450)


draw_graph(graph)
