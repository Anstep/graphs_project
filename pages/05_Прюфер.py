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
    if st.button("Сгенерировать код", type="primary"):
        try:
            res = Algos.encode_prufer(graph)
            if not res and graph.get_vertices_count() == 2:
                st.info("Для дерева из 2 вершин код Прюфера пуст.")
            else:
                st.markdown("### Результат")
                # Красивый математический вывод
                st.latex(f"P = ({', '.join(map(str, res))})")
                # Поле для удобного копирования
                st.code(" ".join(map(str, res)), language="text")
                st.success("Код успешно сформирован")
        except ValueError as e:
            st.error(f"{e}")
            st.stop()
with tab2:
    st.subheader("Декодировать код прюфера")
    user_input = st.text_input(
        "Введите код (через пробел)", placeholder="Напр: 0 1 2 4", key="decode_prufer"
    )
    if st.button("Декодировать", type="primary"):
        code = [int(x) for x in user_input.split()]
        edges_list = Algos.decode_prufer(code)

        st.session_state["decoded_graph"] = GraphFactory.create_from_edges(
            edges=edges_list, n_vertices=len(code) + 2
        )
        st.markdown("### Результат декодирования")
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"Дерево восстановлено")
            st.write(f"Вершин: {len(code) + 2}, Ребер: {len(edges_list)}")
        with col2:
            # Красивый список ребер
            formatted_edges = [f"V{u} ↔ V{v}" for u, v in edges_list]
            st.expander("Список ребер", expanded=True).write(", ".join(formatted_edges))
#  Визуализация
st.divider()
st.subheader("Визуализация")

# логика переключения между восстановленным и исходными графами
if st.session_state.get("decoded_graph") is not None:
    st.info("Отображается дерево, восстановленное из кода Прюфера.")
    if st.button("Вернуться к исходному графу"):
        st.session_state["decoded_graph"] = None
        st.rerun()
    graph = st.session_state["decoded_graph"]

draw_graph(graph)
# apply_custom_styles()
