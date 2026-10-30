# UBL Kernel Contract (v1.0 Frozen)

This public copy mirrors the frozen primitive runtime contract used by the private implementation. Extensions may compose these laws but cannot redefine them.

1. **Eight-bit atom.** Bit 0 is the M-bit. Bits 7:1 are the unsigned seven-bit payload: `payload = atom >> 1`, `M = atom & 1`.
2. **Memory split.** Non-control `M=0` atoms replace volatile state. Non-control `M=1` atoms append one occurrence to the monotonic ledger.
3. **Control precedence.** `SYNC`, `START`, `END`, `ESC`, `PATCH_HEADER`, `WHY`, and `RESET` are decoded before memory routing, independently of M.
4. **Occurrence identity.** Every incoming atom occurrence advances `n` and produces `E_n = SHA256(E_(n-1) || Atom_n || uint64_be(n))`. Equal atoms at different indices remain distinct.
5. **Immutable causality.** Committed ledger entries and EventIDs are append-only and ordered. WHY is a non-mutating query.
6. **RESET.** RESET clears volatile state and returns the framing FSM to IDLE while preserving the persistent ledger. It is itself an occurrence in the execution identity chain.
7. **Base128 envelopes.** Binary manifests use canonical seven-bit chunks. Reserved payloads embedded as data are preceded by ESC. Transport headers such as `A5 5A` remain outside the Base128 body.
8. **Observable parity.** Identical valid atoms yield identical volatile state, ledger contents, FSM state, occurrence EventIDs, and canonical execution hash. Minimal RTL exports state events; the conformance host derives its cryptographic overlay from the same occurrences.

## Two independent histories

### Execution Identity Chain (EventID)

The identity chain records **every incoming U-Atom occurrence**, including transient atoms, framing controls, malformed atoms, `SYNC`, and `RESET`.

`E_n = H(E_(n-1) || Atom_n || uint64_be(n))`

The previous EventID and occurrence index make repeated identical atoms position-dependent. Control processing or rejection may prevent a semantic state mutation, but it does not erase the fact that the atom was observed.

### Semantic State (Monotonic Ledger)

The monotonic ledger is the append-only history of committed, non-control atoms whose M-bit is one. Its head changes only after a valid persistent state mutation. Transient atoms (`M=0`), control tokens, rejected atoms, and `RESET` do not alter the ledger or its head. `RESET` clears volatile state only.

Two executions can therefore have the same semantic ledger head while having different EventID heads—for example, after different transient/control traffic.

## Frozen control payloads

- `00` — SYNC
- `01` — START
- `02` — END
- `03` — ESC
- `7D` — PATCH_HEADER
- `7E` — WHY
- `7F` — RESET

Volatile state persists across END and clears only on RESET or an explicit runtime restoration.
