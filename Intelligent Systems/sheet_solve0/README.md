# Sheet Zero - Graph Toolkit

This project contains a reusable graph class for CSC4103.

## Files
- `code/graph.py`: graph class and search algorithms.
- `code/init.py`: exports the Graph class.
- `tests/test.py`: tests for the graph functions.

## Features
- Directed and undirected graphs
- Default edge weight of 1
- Loading a graph from JSON text
- BFS for a path with the fewest edges
- Dijkstra for the lowest-cost path
- A* with a heuristic function
- Checks for negative and invalid weights

## Run the tests
Open a terminal in the `sheetzero` folder and run:

```bash
python -m unittest discover -s tests -v
```
