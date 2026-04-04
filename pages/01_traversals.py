import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from graph import Graph
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Обходы")

# Ввод графа
matrix, adj_list, viz_matrix, processor = run_graph_input()

# Algo selection
tab1, tab2, tab3, tab4 = st.tabs(
    ["1. Показ DFS", "2. Проверка DFS", "3. Показ BFS", "4. Проверка BFS"]
)

# Обработка
with tab1:
    st.subheader("Демонстрация обхода в глубину")
    # Код алгоритма и визуализация для задачи 1
    if st.button("Запустить DFS"):
        # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
        result = (
            processor.get_dfs(start_node)
            if "DFS" in page
            else processor.get_bfs(start_node)
        )
        st.success(f"Порядок обхода: {' → '.join(map(str, result))}")
        st.session_state["traversal_result"] = result

with tab2:
    st.subheader("Проверьте свои знания DFS")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="DFS"
    )
    if st.button("Проверить DFS"):
        try:
            user_list = list(map(int, user_input.split()))
            if processor.verify_dfs(user_list):
                st.balloons()
                st.success("Верно!")
            else:
                st.error(f"Неверно. Ваш ввод: {user_list}")
        except ValueError:
            st.error("Введите целые числа через пробел")

with tab3:
    st.subheader("Демонстрация обхода в ширину")
    # Код алгоритма и визуализация для задачи 1
    if st.button("Запустить BFS"):
        # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
        result = (
            processor.get_dfs(start_node)
            if "DFS" in page
            else processor.get_bfs(start_node)
        )
        st.success(f"Порядок обхода: {' → '.join(map(str, result))}")
        st.session_state["traversal_result"] = result

with tab4:
    st.subheader("Проверьте свои знания BFS")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="BFS"
    )
    if st.button("Проверить BFS"):
        try:
            user_list = list(map(int, user_input.split()))
            if processor.verify_dfs(user_list):
                st.balloons()
                st.success("Верно!")
            else:
                st.error(f"Неверно. Ваш ввод: {user_list}")
        except ValueError:
            st.error("Введите целые числа через пробел")


# Визуализация
st.divider()
st.subheader("Визуализация")

# Подсвечиваем путь, если алгоритм был запущен
highlight = st.session_state.get("traversal_result", None)
draw_graph(viz_matrix, highlight_nodes=highlight)
