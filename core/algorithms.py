from collections import deque
from heapq import heappop, heappush
from math import inf

from numpy._typing import NDArray


class Algos:
    # Задача 0
    @staticmethod
    def get_vertices_degrees(graph):
        pass

    @staticmethod
    def get_eulerian_status(graph):
        pass

    @staticmethod
    def get_bipartite_status(graph):
        pass

    # Задача 1
    @staticmethod
    def get_dfs(graph, start_node) -> list:
        visited = [False] * graph.get_vertices_count()
        order = []

        def _dfs_recursive(node):
            visited[node] = True
            order.append(node)
            for neighbor in range(graph.get_vertices_count()):
                if graph.is_edge(node, neighbor) and not visited[neighbor]:
                    _dfs_recursive(neighbor)

        _dfs_recursive(start_node)
        return order

    # Задача 2
    @staticmethod
    def verify_dfs(graph, user_path) -> list[tuple[int, int]] | bool:
        stack = []
        visited = [False] * graph.get_vertices_count()
        visited[user_path[0]] = True
        stack.append(user_path[0])
        found = False
        # путь для подсветки
        path = []
        for next_i in range(1, len(user_path)):
            next_node = user_path[next_i]
            found = False
            while stack:
                cur_node = stack[-1]
                if graph.is_edge(cur_node, next_node):
                    if not visited[next_node]:
                        path.append(tuple(sorted((cur_node, next_node))))
                        visited[next_node] = True
                        stack.append(next_node)
                        found = True
                        break
                    else:
                        return False
                else:
                    stack.pop()
            if not found:
                # переход на следующую компоненту
                if not visited[next_node] and not stack:
                    visited[next_node] = True
                    stack.append(next_node)
                else:
                    return False
        return path

    # Задача 3
    @staticmethod
    def get_bfs(graph, start_node) -> list:
        visited = [False] * graph.get_vertices_count()
        order = []
        queue = [start_node]
        visited[start_node] = True

        while queue:
            node = queue.pop(0)
            order.append(node)

            for neighbor in range(graph.get_vertices_count()):
                if graph.is_edge(node, neighbor) and not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        return order

    # Задача 4
    @staticmethod
    def verify_bfs(graph, user_path) -> list[tuple[int, int]] | bool:
        start_vertex = user_path[0]
        queue = deque()
        visited = [False] * graph.get_vertices_count()
        visited[start_vertex] = True
        queue.append(start_vertex)
        path = []
        next_i = 1
        while next_i < len(user_path):
            while queue:
                unvisited_neighbors = [
                    v for v, _ in graph.get_neighbors(queue[0]) if not visited[v]
                ]
                if next_i < len(user_path):
                    next_node = user_path[next_i]
                    if next_node in unvisited_neighbors:
                        path.append(tuple(sorted((queue[0], next_node))))
                        visited[next_node] = True
                        queue.append(next_node)
                        next_i += 1
                    else:
                        if unvisited_neighbors:
                            return False
                        queue.popleft()
                else:
                    if unvisited_neighbors:
                        return False
                    queue.popleft()
            if not queue and next_i < len(user_path):
                # переход на следующую компоненту
                start_node = user_path[next_i]
                if visited[start_node]:
                    return False  # Узел уже был в другой компоненте
                visited[start_node] = True
                queue.append(start_node)
                next_i += 1
        return path if next_i == len(user_path) else False

    # Задача 5
    @staticmethod
    def get_connected_components_count(graph) -> int:
        visited = [False] * graph.get_vertices_count()
        count = 0

        for i in range(graph.get_vertices_count()):
            if not visited[i]:
                Algos._dfs_for_components(graph, i, visited)
                count += 1
        return count

    @staticmethod
    def _dfs_for_components(graph, node, visited):
        visited[node] = True
        for neighbor in range(graph.get_vertices_count()):
            if graph.is_edge(node, neighbor) and not visited[neighbor]:
                Algos._dfs_for_components(graph, neighbor, visited)

    # Задача 6
    @staticmethod
    def verify_components_count(graph, user_count) -> bool:
        return (
            True if Algos.get_connected_components_count(graph) == user_count else False
        )

    # Задача 7
    @staticmethod
    def mst_kruskal(graph) -> list:
        edges = []
        for i in range(graph.get_vertices_count()):
            for j in range(i + 1, graph.get_vertices_count()):
                if graph.is_edge(i, j) > 0:
                    edges.append((graph.is_edge(i, j), i, j))
        edges.sort()

        groups = {i: i for i in range(graph.get_vertices_count())}
        mst = []

        for weight, u, v in edges:
            if groups[u] != groups[v]:
                mst.append((u, v, int(weight)))
                old_group = groups[v]
                new_group = groups[u]
                for node in groups:
                    if groups[node] == old_group:
                        groups[node] = new_group
        print(mst)
        return mst

    # Задача 8
    @staticmethod
    def get_shortest_paths_from(
        graph, start_vertex: int
    ) -> tuple[list[int], list[int]] | False:
        # Алгоритм Дейкстры с использованием приоритетной очереди
        d = [inf] * graph.get_vertices_count()
        p_queue = []
        heappush(p_queue, (0, start_vertex))
        d[start_vertex] = 0
        # массив предков для восстановления пути
        pred = [None] * graph.get_vertices_count()
        while p_queue:
            cur_d, cur_v = heappop(p_queue)
            # Оптимизация: в очереди могут лежать несколько длин путей для вершины
            # если вынули из кучи "старое" значение, то его не имеет смысл рассматривать
            if d[cur_v] < cur_d:
                continue
            for vertex, weight in graph.get_neighbors(cur_v):
                if weight < 0:
                    return False
                if d[vertex] > d[cur_v] + weight:
                    d[vertex] = d[cur_v] + weight
                    pred[vertex] = cur_v
                    heappush(p_queue, (d[vertex], vertex))
        return [int(val) if val != inf else -1 for val in d], pred

    @staticmethod
    def is_tree(graph):
        if Algos.get_connected_components_count(graph) != 1:
            return False

    @staticmethod
    def get_shortest_edges_dijkstra(pred: list[int]) -> list[tuple[int, int]]:
        edges = []
        for v, p in enumerate(pred):
            if p is not None:
                edges.append(tuple(((p, v))))
        return edges

    # Задача 9
    @staticmethod
    def get_matrix_shortest_paths(graph) -> NDArray:
        dist = graph.get_adj_matrix()
        for i in range(graph.get_vertices_count()):
            for j in range(graph.get_vertices_count()):
                if i != j and dist[i][j] == 0:
                    dist[i][j] = float("inf")

        for k in range(graph.get_vertices_count()):
            for i in range(graph.get_vertices_count()):
                for j in range(graph.get_vertices_count()):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    # Задача 10
    @staticmethod
    def encode_prufer(graph) -> list | False:
        # Ref:
        # https://cp-algorithms.com/graph/pruefer_code.html
        # https://networkx.org/documentation/stable/_modules/networkx/algorithms/tree/coding.html#to_prufer_sequence
        n = graph.get_vertices_count()
        if n < 2:
            return []

        # edges_count = 0
        # adj_matrix = graph.get_adj_matrix()
        # for i in range(n):
        #     for j in range(i + 1, n):
        #         if adj_matrix[i][j] > 0:
        #             edges_count += 1

        # if edges_count != n - 1 or Algos.get_connected_components_count(graph) != 1:
        #     return False

        # особый случай
        if n == 2:
            return []

        # вычисление предков через dfs подвешиванием за вершину n - 1
        parent = [-1] * n

        def dfs(v):
            for u, _ in graph.get_neighbors(v):
                if u != parent[v]:
                    parent[u] = v
                    dfs(u)

        dfs(n - 1)

        # текущий минимальный номер вершины
        min_index = -1
        n = graph.get_vertices_count()
        degree = [-1] * n
        # вычисление минимального номера вершины
        # и заполнение массива степеней за раз
        for i in range(n):
            degree[i] = len(graph.get_neighbors(i))
            if degree[i] == 1 and min_index == -1:
                min_index = i

        code = []
        leaf = min_index
        # построение с использованием идее о минимальном номере вершины
        for _ in range(n - 2):
            p = parent[leaf]
            code.append(p)
            degree[p] -= 1
            if degree[p] == 1 and p < min_index:
                leaf = p
            else:
                min_index += 1
                while degree[min_index] != 1:
                    min_index += 1
                leaf = min_index

        return code

    # Задача 11
    @staticmethod
    def decode_prufer(list_prufer_code) -> list:
        n = len(list_prufer_code) + 2
        degree = [1] * n
        for x in list_prufer_code:
            degree[x] += 1

        edges = []

        for x in list_prufer_code:
            for y in range(n):
                if degree[y] == 1:
                    edges.append((x, y))
                    degree[x] -= 1
                    degree[y] -= 1
                    break

        last_nodes = [i for i in range(n) if degree[i] == 1]
        edges.append((last_nodes[0], last_nodes[1]))
        return edges

    # Задача 12
    @staticmethod
    def get_coloring(Graph):
        pass
