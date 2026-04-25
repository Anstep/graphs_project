import streamlit as st

from core.algorithms import Algos
from factories import GraphFactory
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
    if st.button("Декодировать"):
        # формирование графа по выводу алгоритма,
        # следует вынести или формировать граф к алгоритме
        # try:
        code = [int(x) for x in user_input.split()]
        edges_list = Algos.decode_prufer(code)

        st.session_state["decoded_graph"] = GraphFactory.create_from_edges(
            edges=edges_list, n_vertices=len(code) + 2
        )

        st.success(f"Дерево успешно восстановлено!")
        st.write(f"Ребра: {edges_list}")
        # except Exception as e:
        #    st.error(f"Ошибка при декодировании: {e}")

#  Визуализация
st.divider()
st.subheader("Визуализация")

# логика переключения между восстановленным и исходными графами
if st.session_state.get("decoded_graph") is not None:
    st.info("Отображается дерево, восстановленное из кода Прюфера.")
    if st.button("Показать исходный граф"):
        st.session_state["decoded_graph"] = None
        st.rerun()
    graph = st.session_state["decoded_graph"]

draw_graph(graph)
