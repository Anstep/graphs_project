import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

import graph
from ui_utils import run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Обходы")

# Ввод графа
matrix, adj_list, viz_matrix, is_directed, processor = run_graph_input(
    force_directed=False
)

# Algo selection
tab1, tab2 = st.tabs(
    [
        "10. Найти код прюфера",
        "11. Проверить код прюфера",
    ]
)

with tab1:
    st.subheader("Найти код прюфера")
    # Код алгоритма и визуализация для задачи 1
    if st.button("Найти"):
        # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
        result = processor.get_connected_components_count()
        st.success(f"Количество компоент: {result}")
        st.session_state["traversal_result"] = result

with tab2:
    st.subheader("Декодировать код прюфера")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="DFS"
    )
    if st.button("Декодировать"):  # TODO
        try:
            # user_input = user_input
            if graph.decode_prufer(user_input):
                st.balloons()
                st.success("Верно!")
            else:
                st.error(f"Неверно. Попробуйте еще раз")
        except ValueError:
            st.error("")  # !!

# --- Визуализация (универсальный блок) ---
st.divider()
st.subheader("Визуализация")


def draw_graph(matrix, path_highlight=None):
    net = Network(
        height="400px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=False,
    )
    for i in range(len(matrix)):
        color = "#55ff00"
        if path_highlight and i in path_highlight:
            color = "#ff4b4b"
        net.add_node(i, label=f"V{i}", color=color)

    rows, cols = np.where(np.triu(np.array(matrix)) > 0)
    for u, v in zip(rows, cols):
        net.add_edge(int(u), int(v), color="#aaaaaa")

    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=450)


# Подсвечиваем путь, если алгоритм был запущен
highlight = st.session_state.get("traversal_result", None)
draw_graph(viz_matrix, path_highlight=highlight)
