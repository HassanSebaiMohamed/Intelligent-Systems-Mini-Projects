# PS01: Smart Irrigation System

A 90-day simulation comparing a smart irrigation agent with a fixed-timer baseline.

## Requirements
- Python 3.10 or newer
- No third-party packages required

## Run the simulation
From this folder:

```bash
python irrigation.py
```

The program evaluates both controllers over 20 reproducible random seeds and reports mean water use, crop-stress days, and pump-on days.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Design
- `Field`: simulates soil moisture, heat/evaporation, rain, and an 80%-accurate weather forecast.
- `SmartIrrigator.perceive`: filters noisy moisture readings using an exponential moving average.
- `SmartIrrigator.decide`: selects irrigation based on estimated moisture and the forecast, while preserving emergency watering.
- `SmartIrrigator.learn`: increases the target moisture after a stress day and slowly relaxes it after safe days.
- `run_fixed_timer`: baseline that irrigates every other day.

## Reproducibility and limits
The same seed produces the same simulation. Water units are abstract model units, not liters. This is an educational toy model, not a validated agronomic controller. Real deployment would need calibrated soil sensors, local crop/soil parameters, forecast integration, safety limits, and field trials.
