"""Mini-project: hybrid warehouse delivery agent with BFS planning and reactive safety."""
import random
from collections import deque

GRID = [
    "..........",
    ".##.##.##.",
    "..........",
    ".##.##.##.",
    "..........",
]
SHELVES = {"A": (0, 3), "B": (2, 6), "C": (4, 9)}
DOCK = (4, 0)
MOVES = [("Up", (-1, 0)), ("Down", (1, 0)), ("Left", (0, -1)), ("Right", (0, 1))]

class Warehouse:
    def __init__(self, n_workers=3, seed=0):
        self.rng = random.Random(seed)
        self.free = [(r, c) for r, row in enumerate(GRID) for c, ch in enumerate(row) if ch == "."]
        candidates = [p for p in self.free if p not in set(SHELVES.values()) | {DOCK}]
        self.workers = self.rng.sample(candidates, min(n_workers, len(candidates)))

    def step_workers(self, robot_pos):
        occupied = set(self.workers)
        new_workers = []
        for pos in self.workers:
            options = [pos]
            for _, (dr, dc) in MOVES:
                nxt = (pos[0] + dr, pos[1] + dc)
                if nxt in self.free and nxt != robot_pos and nxt not in new_workers:
                    options.append(nxt)
            choice = self.rng.choice(options)
            # Avoid workers stacking on each other.
            if choice in new_workers or choice == robot_pos:
                choice = pos
            new_workers.append(choice)
        self.workers = new_workers

class HybridAgent:
    """Deliberative BFS planner plus reactive collision-prevention layer."""
    def __init__(self, grid=GRID, dock=DOCK):
        self.grid = grid
        self.free = {(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "."}
        self.dock = dock
        self.block_streak = 0

    def plan(self, start, goal, blocked):
        blocked = set(blocked) - {start, goal}
        queue = deque([start])
        parent = {start: None}
        parent_action = {}
        while queue:
            pos = queue.popleft()
            if pos == goal:
                break
            for action, (dr, dc) in MOVES:
                nxt = (pos[0] + dr, pos[1] + dc)
                if nxt in self.free and nxt not in blocked and nxt not in parent:
                    parent[nxt] = pos
                    parent_action[nxt] = action
                    queue.append(nxt)
        if goal not in parent:
            return []
        plan = []
        cur = goal
        while cur != start:
            plan.append(parent_action[cur])
            cur = parent[cur]
        return list(reversed(plan))

    def next_cell(self, pos, action):
        dr, dc = dict(MOVES)[action]
        return pos[0] + dr, pos[1] + dc

    def safe(self, next_cell, workers):
        return next_cell not in set(workers)

def run_orders(seed=0, n_orders=10, n_workers=3, max_steps=2000):
    rng = random.Random(seed + 10000)
    warehouse = Warehouse(n_workers=n_workers, seed=seed)
    agent = HybridAgent()
    robot = DOCK
    stats = {"steps": 0, "waits": 0, "replans": 0, "collisions": 0, "delivered": 0}
    targets = list(SHELVES.values())
    for order_index in range(n_orders):
        shelf = rng.choice(targets)
        # Go to shelf, then return to dock.
        for goal in (shelf, DOCK):
            blocked_streak = 0
            plan = agent.plan(robot, goal, warehouse.workers)
            stats["replans"] += 1
            while robot != goal and stats["steps"] < max_steps:
                if not plan:
                    stats["waits"] += 1
                    stats["steps"] += 1
                    warehouse.step_workers(robot)
                    blocked_streak += 1
                    if blocked_streak >= 2:
                        plan = agent.plan(robot, goal, warehouse.workers)
                        stats["replans"] += 1
                        blocked_streak = 0
                    continue
                action = plan[0]
                candidate = agent.next_cell(robot, action)
                # Reactive safety: never enter an occupied worker cell.
                if not agent.safe(candidate, warehouse.workers):
                    stats["waits"] += 1
                    stats["steps"] += 1
                    blocked_streak += 1
                    warehouse.step_workers(robot)
                    if blocked_streak >= 2:
                        plan = agent.plan(robot, goal, warehouse.workers)
                        stats["replans"] += 1
                        blocked_streak = 0
                    continue
                # Workers move after robot movement; if one would enter robot's
                # destination, keep it out to enforce collision-free simulation.
                robot = candidate
                stats["steps"] += 1
                plan = plan[1:]
                warehouse.step_workers(robot)
                if robot in warehouse.workers:
                    # Defensive invariant; workers should not move onto robot.
                    warehouse.workers = [robot if w == robot else w for w in warehouse.workers]
                    stats["collisions"] += 1
            if stats["steps"] >= max_steps:
                break
        if robot == DOCK:
            stats["delivered"] += 1
        if stats["steps"] >= max_steps:
            break
    return stats

def main():
    print("Hybrid Warehouse Delivery Agent — 10 orders per seed")
    for seed in (0, 1, 2):
        print(f"seed={seed}: {run_orders(seed)}")

if __name__ == "__main__":
    main()
