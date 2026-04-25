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
    st.subheader("Демонстрация обхода в глубину")
    user_start_vertex = st.selectbox(
        label="Вершина",
        options=[v for v in range(graph.get_vertices_count())],
        key="dfs_start_vertex",
    )
    if st.button("Запустить DFS"):
        result = Algos.get_dfs(graph, user_start_vertex)
        st.success(f"Порядок обхода: {' → '.join(map(str, result))}")
        st.session_state["traversal_result"] = result
    pass


with tab2:
    st.subheader("Проверьте свои знания DFS")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="DFS-validate"
    )

    if st.button("Проверить DFS"):
        user_list = list(map(int, user_input.split()))
        path = Algos.verify_dfs(graph, user_list)
        if path:
            st.success("Верно!")
            st.session_state["traversal_result"] = path
        else:
            st.error(f"Неверно. Ваш ввод: {user_input}")


with tab3:
    st.subheader("Демонстрация обхода в ширину")
    user_start_vertex = st.selectbox(
        label="Вершина",
        options=[v for v in range(graph.get_vertices_count())],
        key="bfs_start_vertex",
    )
    if st.button("Запустить BFS"):
        result = Algos.get_bfs(graph, user_start_vertex)
        st.success(f"Порядок обхода: {' → '.join(map(str, result))}")
        st.session_state["traversal_result"] = result
    pass

with tab4:
    st.subheader("Проверьте свои знания BFS")
    user_input = st.text_input(
        "Введите обход (через пробел)", placeholder="Напр: 0 1 2 4", key="BFS-validate"
    )
    if st.button("Проверить BFS"):
        user_list = list(map(int, user_input.split()))
        path = Algos.verify_bfs(graph, user_list)
        if path:
            st.success("Верно!")
            st.session_state["traversal_result"] = path
        else:
            st.error(f"Неверно. Ваш ввод: {user_input}")


# Визуализация
st.divider()
st.subheader("Визуализация")

# Инициализация состояний для визуализации
if "traversal_result" not in st.session_state:
    st.session_state["traversal_result"] = None

# Подсвечиваем путь, если алгоритм был запущен
traversal_edges = st.session_state.get("traversal_result", [])

draw_graph(graph, highlight_edges=traversal_edges)
