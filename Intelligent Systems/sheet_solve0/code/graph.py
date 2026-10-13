import heapq
import json
import math
from collections import deque


class Graph:
    def __init__(self, directed=False):
        # Store each node and its neighbors
        self.adj = {}
        self.directed = directed

    def add_edge(self, u, v, w=1):
        # Check the edge values
        if not isinstance(u, str) or not isinstance(v, str):
            raise TypeError("Node names must be strings")
        if not isinstance(w, (int, float)) or isinstance(w, bool):
            raise TypeError("Weight must be a number")
        if not math.isfinite(w):
            raise ValueError("Weight must be finite")
        if w < 0:
            raise ValueError("Weight cannot be negative")

        # Add nodes if they are new
        self.adj.setdefault(u, {})
        self.adj.setdefault(v, {})

        # Save the edge
        self.adj[u][v] = w

        # Add the reverse edge for an undirected graph
        if not self.directed:
            self.adj[v][u] = w

    def neighbors(self, u):
        # Return neighbors and their weights
        return self.adj.get(u, {}).items()

    @classmethod
    def from_json(cls, text):
        # Convert JSON text into Python data
        try:
            data = json.loads(text)
        except (TypeError, json.JSONDecodeError) as error:
            raise ValueError("Invalid JSON") from error

        if not isinstance(data, dict):
            raise ValueError("JSON must be an object")

        directed = data.get("directed", False)
        edges = data.get("edges")

        if not isinstance(directed, bool):
            raise ValueError("directed must be true or false")
        if not isinstance(edges, list):
            raise ValueError("edges must be a list")

        graph = cls(directed)

        for edge in edges:
            if not isinstance(edge, list) or len(edge) not in (2, 3):
                raise ValueError("Each edge must have 2 or 3 values")

            u, v = edge[0], edge[1]
            weight = edge[2] if len(edge) == 3 else 1
            graph.add_edge(u, v, weight)

        return graph

    def bfs(self, start, goal):
        # Find a path with the fewest edges
        if start not in self.adj or goal not in self.adj:
            return None, 0

        queue = deque([start])
        parent = {start: None}
        expanded = 0

        while queue:
            node = queue.popleft()
            expanded += 1

            if node == goal:
                return self.build_path(parent, goal), expanded

            for neighbor in self.adj[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)

        return None, expanded

    def dijkstra(self, start, goal):
        # Find the path with the lowest total weight
        if start not in self.adj or goal not in self.adj:
            return None, math.inf

        distances = {start: 0}
        parent = {start: None}
        heap = [(0, start)]

        while heap:
            cost, node = heapq.heappop(heap)

            # Skip an old result if a better one was found
            if cost != distances.get(node, math.inf):
                continue

            if node == goal:
                return self.build_path(parent, goal), cost

            for neighbor, weight in self.neighbors(node):
                new_cost = cost + weight

                if new_cost < distances.get(neighbor, math.inf):
                    distances[neighbor] = new_cost
                    parent[neighbor] = node
                    heapq.heappush(heap, (new_cost, neighbor))

        return None, math.inf

    def astar(self, start, goal, h):
        # Use the cost so far and an estimate to the goal
        if start not in self.adj or goal not in self.adj:
            return None, math.inf

        def heuristic(node):
            value = h(node)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError("Heuristic must return a number")
            if not math.isfinite(value) or value < 0:
                raise ValueError("Heuristic must be finite and non-negative")
            return value

        g_score = {start: 0}
        parent = {start: None}
        heap = [(heuristic(start), 0, start)]

        while heap:
            _, cost, node = heapq.heappop(heap)

            if cost != g_score.get(node, math.inf):
                continue

            if node == goal:
                return self.build_path(parent, goal), cost

            for neighbor, weight in self.neighbors(node):
                new_cost = cost + weight

                if new_cost < g_score.get(neighbor, math.inf):
                    g_score[neighbor] = new_cost
                    parent[neighbor] = node
                    priority = new_cost + heuristic(neighbor)
                    heapq.heappush(heap, (priority, new_cost, neighbor))

        return None, math.inf

    @staticmethod
    def build_path(parent, goal):
        # Rebuild the path using the parent nodes
        path = []
        node = goal

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path
