import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from irrigation import Field, SmartIrrigator, run_smart, run_fixed_timer, evaluate

class IrrigationTests(unittest.TestCase):
    def test_field_moisture_stays_in_range(self):
        f = Field(1)
        for _ in range(100):
            heat, rain, _ = f.weather()
            f.step(0.1, heat, rain)
            self.assertGreaterEqual(f.moisture, 0.0)
            self.assertLessEqual(f.moisture, 1.0)

    def test_perception_filters_sensor_noise(self):
        a = SmartIrrigator(target=0.6)
        estimate = a.perceive(1.0)
        self.assertLess(estimate, 1.0)
        self.assertGreater(estimate, 0.6)

    def test_rain_forecast_reduces_routine_irrigation(self):
        a = SmartIrrigator(target=0.7)
        with_rain = a.decide(0.55, True)
        without_rain = a.decide(0.55, False)
        self.assertLess(with_rain, without_rain)

    def test_emergency_irrigation_allowed_when_forecast_rain(self):
        a = SmartIrrigator(target=0.7)
        self.assertGreater(a.decide(0.2, True), 0.0)

    def test_learning_raises_target_after_stress(self):
        a = SmartIrrigator()
        before = a.target
        a.learn(True)
        self.assertGreater(a.target, before)

    def test_learning_target_has_upper_bound(self):
        a = SmartIrrigator(target=0.78)
        a.learn(True)
        self.assertLessEqual(a.target, 0.78)

    def test_simulation_runs_90_days(self):
        result = run_smart(4, 90)
        self.assertEqual(set(result), {'water', 'stress_days', 'pump_days'})
        self.assertGreaterEqual(result['water'], 0)
        self.assertLessEqual(result['stress_days'], 90)

    def test_same_seed_is_reproducible(self):
        self.assertEqual(run_smart(10), run_smart(10))

    def test_timer_is_reproducible(self):
        self.assertEqual(run_fixed_timer(10), run_fixed_timer(10))

    def test_evaluation_compares_both_controllers(self):
        result = evaluate(range(3), 10)
        self.assertIn('Smart agent', result)
        self.assertIn('Fixed timer', result)

    def test_timer_runs_pump_every_other_day(self):
        result = run_fixed_timer(2, 10)
        self.assertEqual(result['pump_days'], 5)

if __name__ == '__main__':
    unittest.main()
