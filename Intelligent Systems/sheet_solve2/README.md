# Hybrid Warehouse Delivery Agent

This folder contains the warehouse delivery mini-project only. It excludes the separate exercises.

## Features
- BFS shortest-path planning on a grid warehouse.
- Reactive safety check before moving into a cell.
- Waits if a worker occupies the next cell.
- Re-plans after repeated blocking.
- Evaluates 10 orders for each of three fixed random seeds.

## Requirements
Python 3.10 or newer. No third-party packages are required.

## Run
From the `sheet_solve2` folder:

```bash
python code/warehouse.py
python -m unittest discover -s tests -v
```

## Folder structure
- `code/warehouse.py`: complete mini-project implementation.
- `tests/test_warehouse.py`: automated tests.
- `reports/report.md`: editable report.
- `reports/report.pdf`: report for viewing/submission.
- `VERIFICATION.txt`: test and simulation output.

Note: zero collisions is a result of this simplified simulation only, not a real-world safety guarantee.
