import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from warehouse import HybridAgent, run_orders, DOCK, SHELVES, GRID

class WarehouseMiniProjectTests(unittest.TestCase):
    def test_bfs_reaches_shelf(self):
        agent = HybridAgent()
        plan = agent.plan(DOCK, SHELVES["A"], [])
        self.assertTrue(plan)
        pos = DOCK
        for action in plan:
            pos = agent.next_cell(pos, action)
        self.assertEqual(pos, SHELVES["A"])

    def test_safety_rejects_occupied_cell(self):
        agent = HybridAgent()
        occupied = (2, 2)
        self.assertFalse(agent.safe(occupied, [occupied]))
        self.assertTrue(agent.safe((2, 3), [occupied]))

    def test_blocked_cells_are_avoided_by_planner(self):
        agent = HybridAgent()
        blocked = {(2, 1), (1, 0)}
        plan = agent.plan(DOCK, SHELVES["A"], blocked)
        self.assertTrue(plan)
        pos = DOCK
        for action in plan:
            pos = agent.next_cell(pos, action)
            self.assertNotIn(pos, blocked)

    def test_three_seeds_deliver_ten_orders_without_simulated_collisions(self):
        for seed in (0, 1, 2):
            stats = run_orders(seed=seed, n_orders=10)
            self.assertEqual(stats["delivered"], 10)
            self.assertEqual(stats["collisions"], 0)
            self.assertGreater(stats["steps"], 0)
            self.assertGreaterEqual(stats["waits"], 0)
            self.assertGreaterEqual(stats["replans"], 0)

if __name__ == "__main__":
    unittest.main()
