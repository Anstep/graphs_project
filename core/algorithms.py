from collections import deque
from heapq import heappop, heappush
from math import inf


class Algos:
    #
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
    def get_dfs(graph, start_vertex) -> list:
        pass

    # Задача 2
    @staticmethod
    def verify_dfs(graph, user_path) -> list[tuple[int, int]] | bool:
        """ """
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
    def get_bfs(graph, start_vertex) -> list:
        pass

    # Задача 4
    @staticmethod
    def verify_bfs(graph, user_path) -> list[tuple[int, int]] | bool:
        """ """

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
        # visited = [False] * graph.get_vertices_count()
        # count = 0
        # for i in range(graph.get_vertices_count()):
        #     if not visited[i]:
        #         count += 1
        #         stack = [i]
        #         visited[i] = True
        #         while stack:
        #             u = stack.pop()
        #             for v, _ in graph.get_neighbors(u):
        #                 if not visited[v]:
        #                     visited[v] = True
        #                     stack.append(v)
        return count

    # Задача 6
    @staticmethod
    def verify_components_count(graph, user_count) -> bool:
        return (
            True if Algos.get_connected_components_count(graph) == user_count else False
        )

    # Задача 7
    @staticmethod
    def get_minimal_spanning_tree(graph) -> list:
        pass

    # Задача 8
    @staticmethod
    def get_shortest_paths_from(graph, start_vertex: int) -> list[int]:
        n = graph.get_vertices_count()
        d = [inf] * n
        marked = [False] * n
        d[start_vertex] = 0
        for _ in range(n):
            cur_vertex = -1
            for i in range(n):
                if not marked[i] and (cur_vertex == -1 or d[i] < d[cur_vertex]):
                    cur_vertex = i
            if cur_vertex == -1 or d[cur_vertex] == inf:
                break
            marked[cur_vertex] = True
            for vertex, weight in graph.get_neighbors(cur_vertex):
                if weight > 0:
                    d[vertex] = min(d[vertex], d[cur_vertex] + weight)
        return [int(val) if val != inf else -1 for val in d]

    # Задача 9
    @staticmethod
    def get_matrix_shortest_paths():
        pass

    # Задача 10
    @staticmethod
    def encode_prufer(graph) -> list:
        # https://cp-algorithms.com/graph/pruefer_code.html
        n = graph.get_vertices_count()
        leafs = []
        degree = [0] * n
        used = [False] * n
        for i in range(n):
            degree[i] = len(graph.get_neighbors(i))
            if degree[i] == 1:
                heappush(leafs, i)
        code = [-1] * (n - 2)
        for i in range(n - 2):
            leaf = heappop(leafs)
            used[leaf] = True
            digit = 0
            for digit_candidate, _ in graph.get_neighbors(leaf):
                if not used[digit_candidate]:
                    digit = digit_candidate
            # digit = adj_list[leaf][0]
            code[i] = digit
            degree[digit] -= 1
            if degree[digit] == 1:
                heappush(leafs, digit)
        return code

    # Задача 11
    @staticmethod
    def decode_prufer(code) -> graph:
        pass

    # Задача 12
    @staticmethod
    def get_coloring(Graph):
        pass
