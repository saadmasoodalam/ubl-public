# Universal Binary Language — Public Review

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23845298.svg)](https://doi.org/10.5281/zenodo.23845298)

**Author / Architect:** Saad Masood  
**ORCID:** https://orcid.org/0009-0005-0796-7198  
**Kernel baseline:** UBL Kernel v1.0.0  
**Public review release:** v1.0.0-review  
**Version DOI:** https://doi.org/10.5281/zenodo.23845298  
**Concept DOI (all versions):** https://doi.org/10.5281/zenodo.23845297  
**Status:** Frozen kernel contract; public technical review requested

This repository contains a limited public review package for the **Universal Binary Language (UBL)** kernel. The primary implementation repository remains private.

UBL v1.0 defines an 8-bit U-Atom with a seven-bit payload and a Bit-0 memory/persistence routing bit. The public claim is deliberately narrow: ordered U-Atom streams combine deterministic volatile/persistent state routing with occurrence-aware execution identity and a frozen control model.

## Public material

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

If you find a concrete technical issue, please open a GitHub issue and identify the specific rule, assumption, benchmark condition, or failure mode involved.
