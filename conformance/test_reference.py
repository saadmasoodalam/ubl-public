"""Hand-authored public-contract vectors, not copied from private test cases."""
from __future__ import annotations

import hashlib
import subprocess
import sys
import unittest

from conformance.reference import ContractReference, CONTROLS, split_atom

ZERO_SEED = bytes(32)


class KernelPublicContractSubset(unittest.TestCase):
    def test_occurrence_overflow_rejected_without_changing_state(self):
        ref = ContractReference(ZERO_SEED)
        ref.occurrences = 2**64 - 1
        before = ref.snapshot()
        with self.assertRaises(OverflowError):
            ref.feed(0x21)
        self.assertEqual(ref.snapshot(), before)

    def test_cli_rejects_invalid_hex_and_seed_without_traceback(self):
        for args in (['--atoms', 'gg'], ['--atoms', '21', '--eventid-seed', '00']):
            with self.subTest(args=args):
                run = subprocess.run([sys.executable, '-m', 'conformance.reference', *args],
                                     capture_output=True, text=True)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, '')
                self.assertNotIn('Traceback', run.stderr)

    def test_all_256_bit_splits(self):
        for payload in range(128):
            for memory in (0, 1):
                atom = payload * 2 + memory
                self.assertEqual(split_atom(atom), (payload, memory))

    def test_bad_input_rejected_before_identity(self):
        for bad in (-1, 256, 1.2, "21", True):
            with self.assertRaises(ValueError):
                split_atom(bad)

    def test_persist_and_replace(self):
        ref = ContractReference(ZERO_SEED)
        for atom in (0x20, 0x21, 0x21, 0x24):
            ref.feed(atom)
        self.assertEqual(ref.volatile, 0x12)
        self.assertEqual(ref.ledger, [0x10, 0x10])
        self.assertEqual(ref.occurrences, 4)

    def test_reset_preserves_ledger_and_clears_volatile(self):
        ref = ContractReference(ZERO_SEED)
        for atom in (0x21, 0x22, 0xFF):
            ref.feed(atom)
        self.assertEqual(ref.volatile, None)
        self.assertEqual(ref.ledger, [0x10])
        self.assertEqual(ref.frame_state, "IDLE")
        self.assertEqual(ref.occurrences, 3)

    def test_why_does_not_mutate_semantic_history(self):
        ref = ContractReference(ZERO_SEED)
        ref.feed(0x21)
        previous = ref.eventid
        for atom in (0xFC, 0xFD):
            ref.feed(atom)
        self.assertEqual(ref.ledger, [0x10])
        self.assertIsNone(ref.volatile)
        self.assertNotEqual(ref.eventid, previous)
        self.assertEqual(ref.actions[-2:], ["WHY", "WHY"])

    def test_control_precedence_both_memory_values(self):
        for payload, name in CONTROLS.items():
            for memory in (0, 1):
                with self.subTest(control=name, m=memory):
                    ref = ContractReference(ZERO_SEED)
                    action = ref.feed((payload << 1) | memory)
                    self.assertEqual(action, name)
                    self.assertEqual(ref.ledger, [])
                    self.assertIsNone(ref.volatile)
                    self.assertEqual(ref.occurrences, 1)

    def test_escaped_reserved_payload_routes_as_data(self):
        for payload in CONTROLS:
            for memory in (0, 1):
                with self.subTest(payload=payload, m=memory):
                    ref = ContractReference(ZERO_SEED)
                    ref.feed(0x06)  # public ESC control; M=0
                    ref.feed((payload << 1) | memory)
                    self.assertFalse(ref.escape_next)
                    if memory:
                        self.assertEqual(ref.ledger, [payload])
                        self.assertIsNone(ref.volatile)
                    else:
                        self.assertEqual(ref.volatile, payload)
                        self.assertEqual(ref.ledger, [])

    def test_dangling_escape_not_auto_completed(self):
        ref = ContractReference(ZERO_SEED)
        ref.feed(0x06)
        self.assertTrue(ref.snapshot()["pending_escape"])
        self.assertEqual(ref.ledger, [])

    def test_patch_header_is_unresolved_control_not_data(self):
        ref = ContractReference(ZERO_SEED)
        self.assertEqual(ref.feed(0xFB), "PATCH_HEADER")
        self.assertEqual(ref.ledger, [])
        self.assertIn("PATCH_HEADER", ref.unresolved_controls)
        self.assertEqual(ref.frame_state, "UNSPECIFIED")

    def test_explicit_zero_seed_known_hash_vectors(self):
        # These fixed SHA-256 outputs were calculated independently of the
        # reference engine and protect byte layout / index endian / order.
        expected = (
            "c0fb50819ba2d51aa5df6ae59d881355cbfad13ef7025b6a3c629b402969cf15",
            "8c2fc6602d9e5bf6c7c52ff166345659f6e96284125421c88611e3a5b53f92c3",
            "3e58474d51589e1ed9b37918abd2c0e95f8fb1a1a23526a3a77cad4b21579658",
            "59aaa0e117e8f81eece0b7d3760d93526652f8afc83da04f35965c58be46fe6e",
        )
        ref = ContractReference(ZERO_SEED)
        for atom, head in zip((0x21, 0x21, 0xFF, 0xFC), expected):
            ref.feed(atom)
            self.assertEqual(ref.eventid.hex(), head)
        self.assertEqual(ref.ledger, [0x10, 0x10])
        self.assertEqual(ref.occurrences, 4)

    def test_seed_is_explicit_and_not_normative(self):
        ref1 = ContractReference(ZERO_SEED)
        ref2 = ContractReference(bytes([1]) * 32)
        for atom in (0x21, 0x21):
            ref1.feed(atom)
            ref2.feed(atom)
        self.assertNotEqual(ref1.eventid, ref2.eventid)
        for malformed_seed in (b"", b"x" * 31, b"x" * 33):
            with self.assertRaises(ValueError):
                ContractReference(malformed_seed)

    def test_identity_is_for_each_occurrence_including_controls(self):
        ref = ContractReference(ZERO_SEED)
        previous = ref.eventid
        for atom in (0x21, 0x21, 0xFC, 0xFF):
            ref.feed(atom)
            self.assertNotEqual(previous, ref.eventid)
            previous = ref.eventid
        self.assertEqual(ref.occurrences, 4)


if __name__ == "__main__":
    unittest.main()
