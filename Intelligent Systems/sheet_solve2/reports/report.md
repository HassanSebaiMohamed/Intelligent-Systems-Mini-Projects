# Hybrid Warehouse Delivery Agent

## Mini-Project Report

### 1. Problem and objective

A warehouse robot collects items from shelves A, B, and C and returns each item to the dock while human workers move unpredictably. The goal is to complete ten orders with fewer steps and waits, appropriate re-planning, and no worker-cell entries in the simulation.

### 2. PEAS description

- **Performance:** Deliver all 10 orders, achieve zero simulated collisions, and reduce movement steps, waits, and unnecessary re-planning.
- **Environment:** A warehouse grid containing shelves A, B, and C, a dock, and moving human workers.
- **Actuators:** Move Up, Down, Left, Right, or wait.
- **Sensors:** Robot position, known grid layout, shelf and dock locations, and current worker positions.

### 3. Environment classification: seven dimensions

1. **Partially observable:** Current worker positions are observed, but their future positions are unknown.
2. **Multi-agent:** The robot shares the warehouse with human workers.
3. **Stochastic:** Worker movement includes random choices.
4. **Sequential:** Each action affects the robot's next position and later route decisions.
5. **Dynamic:** Workers can move while the robot is operating.
6. **Discrete:** Locations and actions are represented using grid cells and discrete moves.
7. **Known layout and transitions, uncertain worker behavior:** The grid and robot movement rules are known, but future worker actions are not.

### 4. Architecture

```text
Order queue → Deliberative BFS planner → Proposed next cell
                    ↑                              ↓
             Re-plan around workers ← Reactive safety check
                                                   ↓
                                  Move if free; otherwise wait
```

The deliberative layer uses breadth-first search (BFS) to compute a shortest path on the unweighted grid. The reactive layer checks the next cell immediately before the robot moves. If a worker occupies that cell, the robot waits rather than entering it. After two consecutive blocked attempts, the agent re-plans using the latest worker positions.

### 5. Evaluation

Ten randomly selected shelf orders were run for each of three fixed seeds. Each order consists of visiting a shelf and returning to the dock.

| Seed | Steps | Waits | Re-plans | Collisions | Orders delivered |
|---:|---:|---:|---:|---:|---:|
| 0 | 223 | 27 | 32 | 0 | 10 |
| 1 | 183 | 11 | 25 | 0 | 10 |
| 2 | 227 | 27 | 32 | 0 | 10 |

Steps include movement and waiting steps. The figures are reproducible for this implementation and these seed values.

### 6. Why a hybrid agent?

A purely reactive agent can avoid an immediate obstacle but may move inefficiently or fail to choose a useful route to a shelf. A purely deliberative planner can compute a good route, but its plan may become outdated when workers move. The hybrid design combines BFS planning for efficient navigation with a reactive safety check for immediate responses to occupied cells. Re-planning after repeated blocking helps the robot adapt to changes.

### 7. Limitations and safety

This is a simplified grid-world simulation. It assumes current worker positions are sensed accurately and uses randomized worker movement rather than realistic human motion. It does not model robot size, speed, braking distance, occlusion, or sensor delay. Zero simulated collisions is not a real-world safety guarantee. A physical system would require reliable sensing, a safety-rated stop, conservative distance margins, extensive testing, and human oversight.
