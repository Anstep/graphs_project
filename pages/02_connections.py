import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Обходы")

# Ввод графа
matrix, adj_list, viz_matrix, processor = run_graph_input()


# Algo selection
tab1, tab2 = st.tabs(
    ["5. Подсчет числа компонент связности", "6. Проверка числа компонент связности"]
)

# Обработка
with tab1:
    st.subheader("Подсчет числа компонент связности")
    # Код алгоритма и визуализация для задачи 1
    if st.button("Подсчитать"):
        # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
        result = processor.get_connected_components_count()
        st.success(f"Количество компоент: {result}")
        st.session_state["traversal_result"] = result

with tab2:
    st.subheader("Проверка числа компонент связности")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 2", key="component_count"
    )
    if st.button("Проверить"):
        try:
            user_input = user_input
            if processor.verify_components_count(user_input):
                st.balloons()
                st.success("Верно!")
            else:
                st.error(f"Неверно. Попробуйте еще раз")
        except ValueError:
            st.error("")  # !!

# Подсвечиваем путь, если алгоритм был запущен
# Визуализация
st.divider()
st.subheader("Визуализация")

draw_graph(viz_matrix)
