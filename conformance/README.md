# UBL — Independent public-contract reference (partial)

This is a **small runnable illustration of the published `KERNEL-CONTRACT.md`**, written from the public document only. It does **not** import the private kernel, reproduce its hardware implementation, or expose the private test infrastructure.

## Reproduce locally

Requires Python 3.11+ and only the standard library:

```sh
python -m conformance.demo
python -m conformance.demo --readings 69 70 71 --threshold 71
python -m unittest discover -s conformance -p 'test_*.py' -v
python -m conformance.reference --atoms '21 22 ff 21'
```

The temperature example is ordinary Python application code over this reference:
every reading updates transient state, while readings at/above the chosen
threshold also append an alarm. Repeated alarms are retained, reserved literal
values are escaped, and the default ledger is `[70,75,75,125]`. Edit
[demo.py](demo.py) or its `--readings`/`--threshold` arguments; `--json` prints a
structured trace. It emits no transport frame and measures no clocks or speed.

The raw-atom CLI prints the final EventID head, semantic ledger, volatile state,
actions for all occurrences, and any unresolved controls. Its default `E_0` is
**32 zero bytes for illustration**, *not* an official kernel seed. Supply your
own with `--eventid-seed` (64 hexadecimal characters).

## What is independently checked

- All 256 possible `(7-bit payload, Bit-0 M)` pairs split correctly.
- Non-control `M=0` replaces transient state; `M=1` appends to the ledger.
- `RESET` clears volatile state and leaves the ledger unchanged.
- `WHY` is semantically non-mutating; each occurrence still changes EventID.
- Both M values of each published control are decoded before ordinary data routing.
- `ESC` makes the next reserved payload literal data.
- Repeated identical input atoms get different occurrence-based EventIDs.
- A known fixed hash trace checks `SHA256(previous32 || atom1 || uint64_be(index))`.

The test methods include exhaustive bit-split loops, independent known hash
vectors, editable-example histories and CLI error checks. Test counts are
reported by the command and public CI; they are not independent mathematical
proofs or the private cross-runtime conformance suite. Outsiders can inspect,
alter and extend these tests.

## Important limits

This is **not** a complete reference implementation or full formal conformance harness. The frozen public document does not fully specify framing states on malformed streams, `PATCH_HEADER` effects beyond control precedence, the initial `E_0` seed, the canonical execution hash, or a ledger-head hash. This reference explicitly marks framing/patch effects as unspecified and deliberately does not invent their behavior. `volatile=None` is an illustrative cleared/unset value, not a hardware register encoding.

The model does not simulate capacity limits, resource usage, persistent power-loss storage, byte transportation, or event hashing in RTL. It is not proof of novelty, compactness, or silicon performance. The UBL public contract and this prototype may have ambiguities or defects; please report concrete counterexamples by opening an issue.

**Authority:** [Public frozen kernel contract](../KERNEL-CONTRACT.md), not private RTL.
