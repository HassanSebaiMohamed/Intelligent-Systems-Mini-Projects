"""Smart irrigation mini-project for Intelligent Systems Practical Sheet 1.

Only Python's standard library is required. Run: python irrigation.py
"""
from __future__ import annotations
from dataclasses import dataclass
import random
import statistics
from typing import Dict, List, Tuple

DAYS = 90

@dataclass
class DayResult:
    water: float
    stress: bool
    pump_on: bool
    moisture: float

class Field:
    """Small deterministic-by-seed model of soil moisture and weather."""
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.moisture = 0.62
        self.day = 0

    def weather(self) -> Tuple[float, bool, bool]:
        """Return heat loss, actual rain, and an 80%-accurate rain forecast."""
        heat_loss = self.rng.uniform(0.025, 0.075)
        actual_rain = self.rng.random() < 0.20
        forecast_correct = self.rng.random() < 0.80
        forecast_rain = actual_rain if forecast_correct else not actual_rain
        return heat_loss, actual_rain, forecast_rain

    def step(self, irrigation: float, heat_loss: float, actual_rain: bool) -> bool:
        # Irrigation and rain increase soil moisture; heat/evaporation reduce it.
        rain_gain = self.rng.uniform(0.10, 0.22) if actual_rain else 0.0
        self.moisture = max(0.0, min(1.0, self.moisture + irrigation + rain_gain - heat_loss))
        self.day += 1
        # Crop stress occurs when soil moisture falls below the critical threshold.
        return self.moisture < 0.30

class SmartIrrigator:
    """Agent with perception filtering, forecast knowledge, and feedback learning."""
    def __init__(self, target: float = 0.62):
        self.target = target
        self.filtered_moisture = target
        self.previous_irrigation = 0.0
        self.stress_last_day = False

    def perceive(self, raw_sensor: float) -> float:
        # Exponential moving average reduces the effect of noisy readings.
        self.filtered_moisture = 0.70 * self.filtered_moisture + 0.30 * raw_sensor
        return self.filtered_moisture

    def decide(self, moisture_estimate: float, forecast_rain: bool) -> float:
        deficit = max(0.0, self.target - moisture_estimate)
        # Forecast reduces routine watering, but never blocks emergency watering.
        if forecast_rain and moisture_estimate > 0.40:
            amount = min(0.10, deficit * 0.55)
        else:
            amount = min(0.16, deficit * 0.95)
        self.previous_irrigation = amount
        return amount

    def learn(self, stress: bool) -> None:
        # Feedback: raise the target after stress; relax very slowly after safe days.
        if stress:
            self.target = min(0.78, self.target + 0.025)
        else:
            self.target = max(0.60, self.target - 0.001)
        self.stress_last_day = stress

def run_smart(seed: int, days: int = DAYS) -> Dict[str, float]:
    field = Field(seed)
    agent = SmartIrrigator()
    water = 0.0
    stress_days = 0
    pump_days = 0
    for _ in range(days):
        heat, rain, forecast = field.weather()
        # Simulated sensor noise, clipped to physically possible range.
        sensor = max(0.0, min(1.0, field.moisture + field.rng.gauss(0.0, 0.055)))
        estimate = agent.perceive(sensor)
        amount = agent.decide(estimate, forecast)
        stress = field.step(amount, heat, rain)
        agent.learn(stress)
        water += amount
        stress_days += int(stress)
        pump_days += int(amount > 0.005)
    return {"water": water, "stress_days": stress_days, "pump_days": pump_days}

def run_fixed_timer(seed: int, days: int = DAYS) -> Dict[str, float]:
    field = Field(seed)
    water = 0.0
    stress_days = 0
    pump_days = 0
    for day in range(days):
        heat, rain, _forecast = field.weather()
        amount = 0.13 if day % 2 == 0 else 0.0
        stress = field.step(amount, heat, rain)
        water += amount
        stress_days += int(stress)
        pump_days += int(amount > 0.005)
    return {"water": water, "stress_days": stress_days, "pump_days": pump_days}

def evaluate(seeds=range(20), days: int = DAYS) -> Dict[str, Dict[str, float]]:
    smart = [run_smart(seed, days) for seed in seeds]
    fixed = [run_fixed_timer(seed, days) for seed in seeds]
    return {
        "Smart agent": {key: statistics.mean(row[key] for row in smart) for key in smart[0]},
        "Fixed timer": {key: statistics.mean(row[key] for row in fixed) for key in fixed[0]},
    }

def main() -> None:
    results = evaluate(range(20), DAYS)
    print(f"Results: 20 random seeds, {DAYS} days per seed")
    print(f"{'Controller':<16}{'Water (units)':>15}{'Stress days':>15}{'Pump-on days':>15}")
    for name, values in results.items():
        print(f"{name:<16}{values['water']:>15.2f}{values['stress_days']:>15.2f}{values['pump_days']:>15.2f}")
    smart, fixed = results['Smart agent'], results['Fixed timer']
    saving = 100 * (fixed['water'] - smart['water']) / fixed['water']
    print(f"Water saved by smart agent: {saving:.1f}%")

if __name__ == '__main__':
    main()
