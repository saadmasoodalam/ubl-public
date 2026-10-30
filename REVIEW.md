# UBL External Review Questions

This page is for reviewers who want to challenge the UBL Kernel v1.0 baseline without access to the private implementation repository.

Please focus on concrete failure cases, prior art, or specification ambiguity.

## Kernel semantics

1. Is the Bit-0 volatile/persistent routing model technically distinct from existing tagged-state or event-sourcing patterns, or is it mainly a compact encoding of known ideas?
2. Are there ambiguous cases where control precedence and the M-bit could produce conflicting interpretations?
3. Does the RESET rule preserve enough state to remain deterministic under restoration/replay?

## Event identity

4. Does `E_n = SHA256(E_(n-1) || Atom_n || uint64_be(n))` provide a useful execution identity beyond a conventional append-only event hash chain?
5. Are there failure modes when identity-chain history and semantic-ledger history diverge intentionally?
6. Should occurrence identity remain part of the kernel contract, or should it be an optional runtime overlay?

## Formal methods

7. Which safety or liveness properties are missing from the current finite-model verification boundary?
8. What assumptions in the lowered FSM model could hide implementation or hardware failures?

## Hardware / runtime parity

9. Is the split between minimal RTL state events and host-derived cryptographic identity defensible, or should the hardware implementation own more of the identity layer?
10. What conformance vectors or fault-injection cases would you require before trusting cross-runtime parity?

## Benchmarking

11. Are the published UBL/TLV/Protobuf/JSON comparisons semantically fair?
12. What workload would be a stronger neutral benchmark?

## Prior art

If you know of a protocol, ISA, event system, tagged architecture, state machine, or hardware mechanism that substantially overlaps with UBL, please provide the exact reference and the overlapping mechanism.

## How to respond

A useful review can be as small as one concrete counterexample. Please identify the relevant rule and explain the failure mode or prior-art relationship.
