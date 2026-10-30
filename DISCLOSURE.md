# UBL Public Disclosure Boundary

This repository is intended for technical review while the primary UBL implementation remains private.

## Public

The following may be discussed and cited publicly:

- the frozen UBL Kernel v1.0 primitive contract
- the 8-bit U-Atom layout
- volatile (`M=0`) versus persistent (`M=1`) routing semantics
- frozen control payloads
- the dual-history distinction between execution identity and semantic persistent state
- the occurrence-aware EventID formula
- the bounded formal-verification contract
- published cross-runtime validation claims
- the published 4-event wire-density benchmark
- public whitepapers and review questions

## Private / withheld

The following are intentionally not included in this package:

- full private source repository
- compiler/runtime implementation internals
- complete RTL source and synthesis implementation details
- private conformance and fault-injection test infrastructure
- carrier/PHY implementation details
- unreleased protocol extensions
- experimental UCO encoding work
- patent-sensitive mechanisms or unpublished hardware designs
- credentials, CI secrets, private build artifacts, or internal development notes

## Reviewer access

A reviewer does not need private repository access to critique the public kernel contract, benchmark methodology, formal-verification scope, or architecture assumptions.

Deeper implementation evidence may be shared selectively where appropriate. Public disclosure of additional material should be treated as an explicit decision rather than inferred from this package.
