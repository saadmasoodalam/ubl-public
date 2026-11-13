"""Public examples checked with hand-written expected histories and wire bytes."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

from conformance.demo import temperature_example

ROOT = Path(__file__).resolve().parents[1]


class PublicTemperatureExample(unittest.TestCase):
    def test_default_history_and_escaped_alarm(self):
        result = temperature_example([20, 45, 70, 75, 75, 60, 125])
        self.assertEqual(result['final']['ledger'], [70, 75, 75, 125])
        self.assertEqual(result['final']['volatile'], 125)
        self.assertEqual(result['rows'][0]['alarms'], [])
        self.assertEqual(result['rows'][3]['alarms'], [70, 75])
        self.assertEqual(result['rows'][-1]['atoms'], '06 FA 06 FB')
        self.assertEqual(result['atoms_hex'], '28 5A 8C 8D 96 97 96 97 78 06 FA 06 FB')
        self.assertEqual(result['atom_count'], 13)
        self.assertEqual(result['final']['occurrences'], 13)
        self.assertFalse(result['final']['pending_escape'])

    def test_threshold_changes_history_without_changing_inputs(self):
        readings = [69, 70, 71]
        self.assertEqual(temperature_example(readings, 70)['final']['ledger'], [70, 71])
        self.assertEqual(temperature_example(readings, 71)['final']['ledger'], [71])

    def test_reserved_readings_are_literal_data_including_reset_and_why(self):
        result = temperature_example([0, 1, 2, 3, 125, 126, 127], 0)
        self.assertEqual(result['final']['ledger'], [0, 1, 2, 3, 125, 126, 127])
        self.assertEqual(result['final']['volatile'], 127)
        self.assertEqual(result['atom_count'], 28)
        self.assertEqual(result['final']['controls_with_unspecified_effects'], [])

    def test_invalid_values_are_rejected(self):
        for bad in (True, False, -1, 128, 1.5, '70', None):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    temperature_example([20, bad])
                with self.assertRaises(ValueError):
                    temperature_example([20], bad)

    def test_documented_module_command_outputs_valid_json(self):
        run = subprocess.run([sys.executable, '-m', 'conformance.demo', '--json'],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['final']['ledger'], [70, 75, 75, 125])

    def test_invalid_cli_input_returns_error_without_partial_output(self):
        run = subprocess.run([sys.executable, '-m', 'conformance.demo', '--readings', '20', '128'],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, '')
        self.assertIn('0 to 127', run.stderr)


if __name__ == '__main__':
    unittest.main()
