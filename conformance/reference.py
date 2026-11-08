"""Executable *partial* reference for the published UBL Kernel v1.0 contract.

Source of authority: KERNEL-CONTRACT.md in ubl-public. No private RTL,
private validation vectors, or unpublished implementation techniques used.

This deliberately does not guess the full framing FSM, PATCH_HEADER effects,
canonical execution hash, ledger-head algorithm, or EventID E_0 seed. Clients
supply an E_0 seed; the sample command uses an explicit ALL-ZERO seed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Optional

# Seven-bit payload identifiers from the public frozen contract.
CONTROLS = {
    0x00: "SYNC",
    0x01: "START",
    0x02: "END",
    0x03: "ESC",
    0x7D: "PATCH_HEADER",
    0x7E: "WHY",
    0x7F: "RESET",
}
UNSPECIFIED = ("SYNC", "START", "END", "PATCH_HEADER")


def split_atom(atom: int) -> tuple[int, int]:
    if type(atom) is not int or not 0 <= atom <= 0xFF:
        raise ValueError("U-Atom must be one integer byte (0..255)")
    return atom >> 1, atom & 1


class ContractReference:
    """Reference for **directly specified** primitive behavior, not full conformance.

    Volatile None denotes a cleared/unset value in THIS reference profile;
    the public contract does not define an electrical register reset encoding.
    The public contract also leaves the initial EventID E_0 unspecified.
    """

    def __init__(self, eventid_seed: bytes):
        if not isinstance(eventid_seed, bytes) or len(eventid_seed) != 32:
            raise ValueError("Supply an explicit 32-byte demonstrator E_0 seed")
        self.eventid = eventid_seed
        self.occurrences = 0
        self.volatile: Optional[int] = None
        self.ledger: list[int] = []
        self.escape_next = False
        self.frame_state = "UNSPECIFIED"
        self.unresolved_controls: list[str] = []
        self.actions: list[str] = []

    def feed(self, atom: int) -> str:
        payload, memory = split_atom(atom)
        self.occurrences += 1
        if self.occurrences >= 2**64:
            raise OverflowError("uint64_be(n) no longer represents occurrence")
        self.eventid = hashlib.sha256(
            self.eventid + bytes([atom]) + self.occurrences.to_bytes(8, "big")
        ).digest()

        if self.escape_next:
            self.escape_next = False
            action = self._route_data(payload, memory, escaped=True)
        elif payload == 0x03:
            self.escape_next = True
            action = "ESC"
        elif payload == 0x7F:
            self.volatile = None
            self.frame_state = "IDLE"  # The only FSM transition explicitly fixed here
            action = "RESET"
        elif payload == 0x7E:
            action = "WHY"  # non-mutating query, except occurrence identity
        elif payload in (0x00, 0x01, 0x02, 0x7D):
            action = CONTROLS[payload]
            # Exact framing/patch transitions are not specified publicly.
            self.frame_state = "UNSPECIFIED"
            self.unresolved_controls.append(action)
        else:
            action = self._route_data(payload, memory, escaped=False)

        self.actions.append(action)
        return action

    def _route_data(self, payload: int, memory: int, *, escaped: bool) -> str:
        if memory:
            self.ledger.append(payload)
            return "ESCAPED_PERSIST" if escaped else "PERSIST"
        self.volatile = payload
        return "ESCAPED_TRANSIENT" if escaped else "TRANSIENT"

    def snapshot(self) -> dict:
        return {
            "occurrences": self.occurrences,
            "eventid_hex": self.eventid.hex(),
            "ledger": self.ledger[:],
            "volatile": self.volatile,
            "pending_escape": self.escape_next,
            "framing_state": self.frame_state,
            "controls_with_unspecified_effects": self.unresolved_controls[:],
            "actions": self.actions[:],
            "reference_is_complete_kernel_implementation": False,
        }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Partial public UBL v1.0 reference; not frozen implementation"
    )
    parser.add_argument("--atoms", required=True,
                        help="Whitespace-separated hexadecimal bytes, e.g. '21 22 ff 21'")
    parser.add_argument("--eventid-seed", default="00" * 32,
                        help="Explicit 32-byte E_0 as 64 hex chars; default is demo zero32, NOT specified by contract")
    args = parser.parse_args()
    try:
        stream = bytes.fromhex(args.atoms)
        seed = bytes.fromhex(args.eventid_seed)
    except ValueError as e:
        parser.error(f"invalid hexadecimal input: {e}")
    model = ContractReference(seed)
    for atom in stream:
        model.feed(atom)
    print(json.dumps(model.snapshot(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
