import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Прюфер")

# Ввод графа
graph = run_graph_input(force_directed=False)

# Algo selection
tab1, tab2 = st.tabs(
    [
        "10. Найти код прюфера",
        "11. Проверить код прюфера",
    ]
)

with tab1:
    st.subheader("Найти код прюфера")
    if st.button("Найти"):
        result = Algos.encode_prufer(graph)

        st.success(f"Код: {' '.join(map(str, result))}")

with tab2:
    st.subheader("Декодировать код прюфера")
    user_input = st.text_input(
        "Введите код (через пробел)", placeholder="Напр: 0 1 2 4", key="decode_prufer"
    )
    if st.button("Декодировать"):  # TODO
        try:
            user_input = [int(x) for x in user_input.split(" ")]
            try:
                Algos.decode_prufer(user_input)
            except IndexError e:
                st.error(f"Неверно. Попробуйте еще раз")
                st.stop()
            st.balloons()
            st.success("Верно!")
                st.error(f"Неверно. Попробуйте еще раз")

#  Визуализация
st.divider()
st.subheader("Визуализация")

draw_graph(graph)
