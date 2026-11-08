# UBL v11 — Independent public-contract reference (partial)

This is a **small runnable illustration of the published `KERNEL-CONTRACT.md`**, written from the public document only. It does **not** import the private kernel, reproduce its hardware implementation, or expose the private test infrastructure.

## Reproduce locally

Requires Python 3.11+ and only the standard library:

```sh
python -m unittest discover -s conformance -p 'test_*.py' -v
python -m conformance.reference --atoms '21 22 ff 21'
```

The CLI prints each occurrence's final EventID head, semantic ledger, volatile state, and any unresolved controls. Its default `E_0` is **32 zero bytes for illustration**, *not* an official kernel seed. Supply your own with `--eventid-seed` (64 hexadecimal characters).

## What is independently checked

- All 256 possible `(7-bit payload, Bit-0 M)` pairs split correctly.
- Non-control `M=0` replaces transient state; `M=1` appends to the ledger.
- `RESET` clears volatile state and leaves the ledger unchanged.
- `WHY` is semantically non-mutating; each occurrence still changes EventID.
- Both M values of each published control are decoded before ordinary data routing.
- `ESC` makes the next reserved payload literal data.
- Repeated identical input atoms get different occurrence-based EventIDs.
- A known fixed hash trace checks `SHA256(previous32 || atom1 || uint64_be(index))`.

The 12 `unittest` test methods include exhaustive loops; they are **not 12 independent mathematical proofs**. The tests are only an example set that outsiders can inspect, alter, and extend.

## Important limits

This is **not** a complete reference implementation or full formal conformance harness. The frozen public document does not fully specify framing states on malformed streams, `PATCH_HEADER` effects beyond control precedence, the initial `E_0` seed, the canonical execution hash, or a ledger-head hash. This reference explicitly marks framing/patch effects as unspecified and deliberately does not invent their behavior. `volatile=None` is an illustrative cleared/unset value, not a hardware register encoding.

The model does not simulate capacity limits, resource usage, persistent power-loss storage, byte transportation, or event hashing in RTL. It is not proof of novelty, compactness, or silicon performance. The UBL public contract and this prototype may have ambiguities or defects; please report concrete counterexamples by opening an issue.

**Authority:** [Public frozen kernel contract](../KERNEL-CONTRACT.md), not private RTL.
