# UBL Kernel v1.0 — Native Execution and Practical State-Routing Validation

**Author / architect:** Saad Masood  
**Date:** 2026-11-27  
**Status:** Supplemental research summary; frozen kernel v1.0.0 unchanged.  
**License:** CC BY 4.0 for this public package only.

## Research question

Can a byte carrying seven payload bits and a bit-0 state/persistence action support useful low-level telemetry while preserving an equivalent application and occurrence-identity contract? Does a particular native implementation reduce processing work compared with a conventional packed-byte implementation?

The public [kernel contract](KERNEL-CONTRACT.md) remains unchanged. The M-bit is an action selector for permitted data, not a hardware durability guarantee. Event occurrence identity and committed semantic history are separate. Both are relevant to a fair cost comparison.

## Engineering progress

Private engineering work now includes a compiled native application path, an optional optimized software dispatcher, reusable application policies and a synthetic motor-alarm lifecycle example. Native executables were checked without a Python interpreter at runtime; Python remains a build/test dependency. The original implementation remains the default. The private application correctness suite reported 191 passing software checks without skips and 131,072 bounded prior-state/input comparisons across two dispatcher choices. These counts refer to the scoped November 21 software validation, not a new formal or hardware proof.

Earlier native RTL simulation reported four passing tests, 12,000 changing-input iterations and 56/56 corruption recoveries. That workload primarily challenged a saturated ledger. A separate experiment reported 1,024 accepted appends and 128 rejected overflow attempts. These are simulator results, not measured physical timing or nonvolatile retention.

## Controlled native instruction-count comparison

A private November 22 experiment evaluated three compiled paths: the original UBL implementation, an optional UBL dispatcher and an independently implemented conventional packed8 reference. Each used the same three predetermined synthetic motor-lifecycle workloads, 1,000 input pairs per workload, equivalent state/history outputs, bounded ledger capacity, encoding/escaping and occurrence SHA-256 computation. Each workload/path was profiled once (nine total); correctness gates preceded profiling. The compared region includes initialization/validation, application policy, state processing, canonicalization and occurrence SHA work; file I/O and output are outside that region.

Environment: Ubuntu 24.04 x86-64, GCC 13.3.0, Valgrind/Callgrind 3.22.0, common optimized C99 build flags. The metric is guest instructions (Ir), not wall time, processor cycles, power or energy.

| Workload seed | Original UBL Ir | Optional UBL Ir | Conventional packed8 Ir |
| --- | ---: | ---: | ---: |
| 71237 | 12,019,083 | 11,997,033 | 12,011,880 |
| 8173 | 12,028,854 | 12,006,818 | 12,021,646 |
| 88442 | 12,033,732 | 12,011,703 | 12,026,531 |

Relative to packed8 (the denominator), the optional implementation uses 0.123294–0.123603% fewer instructions. The original uses 0.059876–0.059966% more. The optional implementation's linked executable text is 8,812 bytes versus 8,340 bytes for packed8 (+472); the original is 8,772 bytes. Fixed context, application-state and emission-buffer inventories tie across the paths. Wire-byte counts also tie (2,435 / 2,437 / 2,438 per workload). These inventories are not aggregate process memory or peak stack measurements.

SHA-256 accounts for approximately 96.43% of the optional path's measured instructions and matches across paths for each workload. The study preserves that work in its total. The benefit is specific to the tested implementations and workloads; it does not isolate the action bit as a causal architectural advantage. Packed8 already has the same byte density.

The research report records 213 passing scoped software checks, 196,608 bounded application cases, 6,144 independent consumer contexts and 18 full traces preceding the nine profiles. These are different coverage units, not additive test counts. The archived private evidence was audited against source identities and independent expected traces by the research project. The public archive does not contain the native binaries, source, private vectors or raw profiles. Readers cannot independently reproduce these private instruction numbers from this package; they are author-reported bounded measurements. The runnable example below does **not** reproduce them.

## Runnable public illustration

The independent [public lifecycle example](conformance/lifecycle.py) uses the already published Python contract reference. Its illustrative two-state hysteresis policy is newly written from the public contract, not a port of the private four-state motor policy. Every reading is transient; only a threshold crossing and later recovery append event codes. It demonstrates repeated event occurrences and reserved literal escaping.

Run with Python 3.11+ and no extra packages:

    python -m conformance.lifecycle
    python -m conformance.lifecycle --readings 40 80 82 65 50 80 50
    python -m unittest discover -s conformance -p 'test_*.py' -v

Default readings are 40, 80, 82, 65, 50, 80, 50. With trip threshold 75 and recovery threshold 55, its ledger is [90, 91, 90, 91]. The example uses synthetic values and the public reference's illustrative zero EventID seed, unbounded ledger and symbolic reset value. It is not a motor controller, finite-memory implementation, native benchmark, proof of conformance with private RTL or safety-certified system.

## Limitations and questions for reviewers

- A small instruction-count improvement with a larger executable is a tradeoff, not general superiority. No physical timing, energy, silicon area, or power-loss durability was measured in this software comparison.
- The private historical receiver has a known discrepancy on unescaped PATCH_HEADER (0x7D), which the published contract treats as a control. It remains explicitly unresolved. See [public reference gaps](conformance/GAPS.md). Historical-equivalence results are not full published-contract conformance.
- Earlier FPGA estimates are scoped to the tools, targets and experiments described in [HARDWARE-V4.md](HARDWARE-V4.md); subsequent equal-contract research does not establish a universal hardware winner.
- An append in a receiver's semantic ledger does not establish durable delivery, transport acknowledgment, replay across power cycles or a nonvolatile store.
- No novelty claim is made by these results. What comparator, controls and independent public fixtures would best distinguish representation from implementation and workload effects?

## Citation and disclosure

This supplement accompanies the original runnable public-contract archive, [10.5281/zenodo.24209493](https://doi.org/10.5281/zenodo.24209493), and frozen specification archive, [10.5281/zenodo.23845298](https://doi.org/10.5281/zenodo.23845298). The concept DOI [10.5281/zenodo.23845297](https://doi.org/10.5281/zenodo.23845297) identifies the version family. This update does not replace the older immutable archives. The version-specific DOI for this supplement must be verified after release. No private repository, compiler, RTL, native source, raw profile or unpublished mechanism is released. See [DISCLOSURE.md](DISCLOSURE.md).
