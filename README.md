# Universal Binary Language — Public Review

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23845298.svg)](https://doi.org/10.5281/zenodo.23845298)
[![Public reference tests](https://github.com/saadmasoodalam/ubl-public/actions/workflows/public-conformance.yml/badge.svg?branch=main)](https://github.com/saadmasoodalam/ubl-public/actions/workflows/public-conformance.yml)

**Author / Architect:** Saad Masood  
**ORCID:** https://orcid.org/0009-0005-0796-7198  
**Kernel baseline:** UBL Kernel v1.0.0  
**Public review release:** v1.0.0-review  
**Version DOI:** https://doi.org/10.5281/zenodo.23845298  
**Concept DOI (all versions):** https://doi.org/10.5281/zenodo.23845297  
**Status:** Runnable public-contract reference and frozen-contract review material

This repository contains a limited public review package for the **Universal Binary Language (UBL)** kernel. The primary implementation repository remains private.

You can run, inspect and modify the included Python reference. It is an
independent illustration derived from the published contract, with explicit
limits; it is not a release of the private compiler or RTL.

UBL v1.0 defines an 8-bit U-Atom with a seven-bit payload and a Bit-0 memory/persistence routing bit. The public claim is deliberately narrow: ordered U-Atom streams combine deterministic volatile/persistent state routing with occurrence-aware execution identity and a frozen control model.

## Try it in one minute

Requires **Python 3.11+** and Git. No packages, account, private access or hardware
are required. From a terminal:

```sh
git clone https://github.com/saadmasoodalam/ubl-public.git
cd ubl-public
python -m conformance.demo
```

Use `python3` if that is your Python command. The editable temperature example
updates the current reading with M=0 and appends readings at or above 70 with
M=1. Its default synthetic readings are `20 45 70 75 75 60 125`.
You should see:

```text
Reading  Atom bytes    Current  Alarm ledger
     20  28                 20  []
     45  5A                 45  []
     70  8C 8D              70  [70]
     75  96 97              75  [70, 75]
     75  96 97              75  [70, 75, 75]
     60  78                 60  [70, 75, 75]
    125  06 FA 06 FB       125  [70, 75, 75, 125]
```

Repeated alarms remain separate ledger entries. Value 125 is reserved, so the
example inserts ESC before each literal occurrence. The stream contains 13 atoms,
including those two ESC controls. It does not include transport framing.

Change the inputs and threshold, inspect raw atoms, or run the public tests:

```sh
python -m conformance.demo --readings 69 70 71 --threshold 71
python -m conformance.demo --json
python -m conformance.reference --atoms '21 22 ff 21'
python -m unittest discover -s conformance -p 'test_*.py' -v
```

The changed-threshold example ends with alarm ledger `[71]`.
The raw-atom example ends with ledger `[16,16]` and a cleared current value,
showing that RESET preserves committed history. Read or edit
[conformance/demo.py](conformance/demo.py), inspect the
[reference model](conformance/reference.py), and add a counterexample to the
[public tests](conformance/test_reference.py).

The threshold condition is ordinary Python application code. This example
demonstrates the published state-routing idea; it does not establish novelty,
hardware efficiency, physical persistence, or a general-purpose language runtime.
The model has an unbounded ledger and deliberately leaves unspecified framing
and patch behavior unresolved. Its zero EventID seed and symbolic `None` reset
value are explicit demonstration choices. See [limitations](conformance/GAPS.md).

## Public material

- [conformance/](conformance/README.md) — runnable public-contract reference, editable example and tests
- [KERNEL-CONTRACT.md](KERNEL-CONTRACT.md) — frozen v1.0 primitive laws
- [VERIFICATION.md](VERIFICATION.md) — formal-verification and cross-runtime validation scope
- [BENCHMARKS.md](BENCHMARKS.md) — published wire-density benchmark evidence
- [HARDWARE-V4.md](HARDWARE-V4.md) — November 2026 FPGA simulation, resource mapping and estimated timing (limits stated)
- [REVIEW.md](REVIEW.md) — questions for external technical reviewers
- [DISCLOSURE.md](DISCLOSURE.md) — public/private boundary
- [CITATION.cff](CITATION.cff) — machine-readable citation metadata

## Public whitepaper

https://dadastore.co/research/papers/ubl-kernel-v1.html

## Citation

The live repository now includes an executable illustration. The archived DOI
below identifies the original public-review baseline, not a claim that this
new example or its current CI was included in that archive.

For this exact archived public-review baseline, cite:

> Masood, Saad. *UBL Kernel v1.0 — Public Review and Evidence Baseline*. Version v1.0.0-review, 2026. Zenodo. https://doi.org/10.5281/zenodo.23845298

For references intended to follow the project across future versions, use the concept DOI:

https://doi.org/10.5281/zenodo.23845297

## Feedback requested

The most useful feedback is technical criticism rather than endorsement. In particular:

- prior art or equivalent architectures
- counterexamples to the state-routing model
- ambiguities in the frozen kernel contract
- failure modes in the EventID / monotonic-ledger separation
- benchmark-methodology weaknesses
- formal-model assumptions that are too strong
- hardware/runtime parity concerns

Relevant backgrounds include embedded systems, FPGA/RTL, protocol design, formal methods/SMT, event sourcing, distributed systems, and systems architecture.

## Scope

This public repository does not publish the private implementation repository. Additional implementation material is withheld unless explicitly released.

The included tests exercise this public Python subset. They do not reproduce
the private cross-runtime suite, hardware experiments, formal solver runs or
historical benchmark measurements described in the review documents.

If you find a concrete technical issue, please open a GitHub issue and identify the specific rule, assumption, benchmark condition, or failure mode involved.
