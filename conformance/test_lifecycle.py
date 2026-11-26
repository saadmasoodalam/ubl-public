"""Hand-authored expectations for the public lifecycle example."""
import json
import subprocess
import sys
import unittest
from conformance.lifecycle import DEFAULT, lifecycle


class LifecycleTests(unittest.TestCase):
    def test_default_transitions_and_bytes(self):
        r = lifecycle(DEFAULT)
        self.assertEqual(r["final"]["ledger"], [90, 91, 90, 91])
        self.assertEqual(r["final"]["volatile"], 50)
        self.assertEqual(r["atoms_hex"], "50 A0 B5 A4 82 64 B7 A0 B5 64 B7")
        self.assertEqual(r["atom_count"], 11)
        self.assertEqual(r["final"]["occurrences"], 11)
        self.assertFalse(r["alarm_active"])

    def test_hysteresis_boundaries(self):
        r = lifecycle([74, 75, 75, 56, 55, 55])
        self.assertEqual(r["final"]["ledger"], [90, 91])
        self.assertEqual([x["alarm"] for x in r["rows"]], [False, True, True, True, False, False])

    def test_reserved_readings(self):
        r = lifecycle([0, 125, 127, 126, 3])
        self.assertEqual(r["final"]["ledger"], [90, 91])
        self.assertEqual(r["final"]["volatile"], 3)
        self.assertFalse(r["final"]["pending_escape"])
        self.assertEqual(r["final"]["controls_with_unspecified_effects"], [])

    def test_validation(self):
        for args in [([True],), ([128],), ([1], 40, 40), ([1], 40, 41)]:
            with self.assertRaises(ValueError):
                lifecycle(*args)

    def test_cli(self):
        p = subprocess.run([sys.executable, "-m", "conformance.lifecycle"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["final"]["ledger"], [90, 91, 90, 91])
