import pandas as pd
import streamlit as st

from core.algorithms import Algos
from ui_utils import draw_graph, run_graph_input

# Настройка страницы
st.set_page_config(layout="wide", page_title="Кратчайшие пути")

# Ввод графа
graph = run_graph_input(force_weighted=True)

# Выбор алгоритма
tab1, tab2 = st.tabs(
    [
        "8. Нахождение кратчайших путей от вершины",
        "9. Нахождение матрицы кратчайших путей",
    ]
)

# if st.sidebar.button("🎲 Сгенерировать случайный"):
#     # Логика заполнения st.session_state.matrix_editor случайными 0 и 1
#     pass

with tab1:
    st.subheader("Нахождение кратчайших путей от вершины")
    user_start_vertex = st.selectbox(
        label="Вершина",
        options=[v for v in range(graph.get_vertices_count())],
        key="vertex_dijkstra",
    )
    if st.button("Найти", key="button_dejikstra"):
        try:
            # Сохраняем весь словарь результатов в сессию
            st.session_state["dijkstra_results"] = Algos.get_shortest_paths_from(
                graph, user_start_vertex
            )
            st.session_state["highlight_edges"] = None
        except ValueError as e:
            st.error(f"Ошибка: {e}")
            st.session_state["dijkstra_results"] = None

    # Если результаты есть в сессии, отрисовываем их
    if st.session_state.get("dijkstra_results"):
        res = st.session_state["dijkstra_results"]
        dists = res["distances"]
        preds = res["predecessors"]
        st.markdown("### Результат")
        cols = st.columns(len(dists))
        for i, d in enumerate(dists):
            cols[i].metric(f"V{i}", "∞" if d == -1 else d)

        mode = st.radio("Режим визуализации:", ["Весь остов", "До конкретной вершины"])

        if mode == "Весь остов":
            st.session_state["highlight_edges"] = Algos.get_shortest_edges_dijkstra(
                graph, preds
            )
        else:
            target = st.selectbox("До вершины:", range(graph.get_vertices_count()))
            if dists[target] != -1:
                path = Algos.reconstruct_path_dijkstra(preds, target, user_start_vertex)
                # Из списка вершин нужно получить список ребер для подсветки
                st.session_state["highlight_edges"] = [
                    tuple(((path[i], path[i + 1]))) for i in range(len(path) - 1)
                ]


with tab2:
    st.subheader("Нахождение матрицы кратчайших путей")
    if st.button("Найти", key="button_matrix"):
        st.session_state["highlight_edges"] = None
        dist_matrix = Algos.get_matrix_shortest_paths(graph)
        st.dataframe(pd.DataFrame(dist_matrix))

# Визуализация
st.divider()
st.subheader("Визуализация")

# Инициализация состояний для визуализации
if "highlight_edges" not in st.session_state:
    st.session_state["highlight_edges"] = None

# col1, col2, col3, col4 = st.columns(4)
# col1.metric("Вершин", graph.get_vertices_count())
# col2.metric(
#     "Ребер",
#     sum(len(graph.get_neighbors(i)) for i in range(graph.get_vertices_count()))
#     // (1 if graph.is_directed() else 2),
# )
# col3.metric("Компонент", Algos.get_connected_components_count(graph))
# col4.metric("Эйлеров", "Да" if Algos.is_eulerian(graph) else "Нет")

draw_graph(
    graph,
    highlight_edges=st.session_state.get("highlight_edges"),
)
