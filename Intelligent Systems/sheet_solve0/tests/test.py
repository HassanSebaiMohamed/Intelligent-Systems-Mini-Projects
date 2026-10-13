import math
import sys
import unittest
from pathlib import Path

# Find the code folder when tests are run
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge("A", "B", 2)
        self.graph.add_edge("A", "C", 1)
        self.graph.add_edge("C", "B", 1)
        self.graph.add_edge("B", "D", 3)

    def test_undirected_edges(self):
        self.assertEqual(self.graph.adj["A"]["B"], 2)
        self.assertEqual(self.graph.adj["B"]["A"], 2)

    def test_directed_edges(self):
        graph = Graph(directed=True)
        graph.add_edge("A", "B", 4)
        self.assertIn("B", graph.adj["A"])
        self.assertNotIn("A", graph.adj["B"])

    def test_default_weight(self):
        graph = Graph()
        graph.add_edge("A", "B")
        self.assertEqual(graph.adj["A"]["B"], 1)

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            self.graph.add_edge("A", "B", -1)

    def test_bfs(self):
        path, expanded = self.graph.bfs("A", "D")
        self.assertEqual(path, ["A", "B", "D"])
        self.assertGreater(expanded, 0)

    def test_dijkstra(self):
        path, cost = self.graph.dijkstra("A", "D")
        self.assertEqual(path, ["A", "B", "D"])
        self.assertEqual(cost, 5)

    def test_astar(self):
        heuristic = {"A": 3, "B": 2, "C": 2, "D": 0}
        path, cost = self.graph.astar("A", "D", lambda node: heuristic[node])
        self.assertEqual(path, ["A", "B", "D"])
        self.assertEqual(cost, 5)

    def test_unreachable_goal(self):
        self.graph.add_edge("X", "Y", 1)
        path, cost = self.graph.dijkstra("A", "Y")
        self.assertIsNone(path)
        self.assertTrue(math.isinf(cost))

    def test_bfs_unknown_node(self):
        path, expanded = self.graph.bfs("A", "Z")
        self.assertIsNone(path)
        self.assertEqual(expanded, 0)

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            Graph.from_json("{not valid json}")

    def test_json_loading(self):
        graph = Graph.from_json(
            '{"directed": false, "edges": [["A", "B", 2], ["B", "C"]]}'
        )
        self.assertEqual(graph.adj["A"]["B"], 2)
        self.assertEqual(graph.adj["B"]["C"], 1)
        self.assertEqual(graph.adj["C"]["B"], 1)


if __name__ == "__main__":
    unittest.main()
