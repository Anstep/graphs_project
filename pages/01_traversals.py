import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Обходы")

# Ввод графа
graph = run_graph_input(force_weighted=False)

# Выбор алгоритма
tab1, tab2, tab3, tab4 = st.tabs(
    ["1. Построение DFS", "2. Проверка DFS", "3. Построение BFS", "4. Проверка BFS"]
)

# Обработка
with tab1:
    # st.subheader("Демонстрация обхода в глубину")
    # # Код алгоритма и визуализация для задачи 1
    # if st.button("Запустить DFS"):
    #     # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
    #     result = (
    #         processor.get_dfs(start_node)
    #         if "DFS" in page
    #         else processor.get_bfs(start_node)
    #     )
    #     st.success(f"Порядок обхода: {' → '.join(map(str, result))}")
    #     st.session_state["traversal_result"] = result
    pass


with tab2:
    st.subheader("Проверьте свои знания DFS")
    # TODO ВАЛИДАТОР ВВОДА ОБХОДА
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="DFS-validate"
    )

    if st.button("Проверить DFS"):
        user_list = list(map(int, user_input.split()))
        if Algos.verify_dfs(graph, user_list):
            st.success("Верно!")
            st.session_state["traversal_result"] = user_list
        else:
            st.error(f"Неверно. Ваш ввод: {user_input}")


with tab3:
    # st.subheader("Демонстрация обхода в ширину")  # TODO
    # # Код алгоритма и визуализация для задачи 1
    # if st.button("Запустить BFS"):
    #     # Предполагаем, что методы возвращают список вершин: [0, 1, 3...]
    #     result = (
    #         processor.get_dfs(start_node)
    #         if "DFS" in page
    #         else processor.get_bfs(start_node)
    #     )
    #     st.success(f"Порядок обхода: {' → '.join(map(str, result))}")
    #     st.session_state["traversal_result"] = result
    pass

with tab4:
    st.subheader("Проверьте свои знания BFS")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="BFS-validate"
    )
    if st.button("Проверить BFS"):
        user_list = list(map(int, user_input.split()))
        if Algos.verify_bfs(graph, user_list):
            st.success("Верно!")
            st.session_state["traversal_result"] = user_list
        else:
            st.error(f"Неверно. Ваш ввод: {user_input}")


# Визуализация
st.divider()
st.subheader("Визуализация")

# Инициализация состояний для визуализации
if "traversal_result" not in st.session_state:
    st.session_state["traversal_result"] = None

# Подсвечиваем путь, если алгоритм был запущен
traversal_nodes = st.session_state.get("traversal_result", [])
highlight_edges = []

# Конвертация последовательности вершин в формат для pyviz
if traversal_nodes and len(traversal_nodes) > 1:
    # Создаем пары (u, v) из последовательности вершин
    highlight_edges = [
        (traversal_nodes[i], traversal_nodes[i + 1])
        for i in range(len(traversal_nodes) - 1)
    ]
    st.warning(traversal_nodes)

draw_graph(graph, highlight_edges=highlight_edges)
