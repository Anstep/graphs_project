import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Компоненты")

# Ввод графа
graph = run_graph_input(force_directed=False)

# Algo selection
tab1, tab2 = st.tabs(
    ["5. Подсчет числа компонент связности", "6. Проверка числа компонент связности"]
)

# Обработка
with tab1:
    st.subheader("Подсчет числа компонент связности")
    if st.button("Подсчитать"):
        result = Algos.get_connected_components_count(graph)
        st.success(f"Количество компоент: {result}")
        st.session_state["traversal_result"] = result

with tab2:
    st.subheader("Проверка числа компонент связности")
    user_input = st.text_input(
        "Введите число", placeholder="Напр: 2", key="component_count"
    )

    if st.button("Проверить"):
        try:
            user_input = user_input
            if Algos.verify_components_count(graph, int(user_input)):
                st.balloons()
                st.success("Верно!")
            else:
                st.error(f"Неверно. Попробуйте еще раз")
        except ValueError:
            st.error("")  # !!

# Визуализация
st.divider()
st.subheader("Визуализация")

draw_graph(graph)
