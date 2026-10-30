# UBL v1.0 Verification Scope

This document summarizes the verification claims that are safe to expose publicly. It is intentionally narrower than the private implementation repository.

## Cross-runtime validation

The UBL Kernel v1.0.0 release reports a **328-test differential conformance suite** spanning:

- Python
- C99
- JavaScript / WebAssembly
- Verilog RTL

The release also reports live CI execution for:

- Z3
- Icarus Verilog
- Yosys
- GCC C99
- Node.js / WebAssembly

The purpose of the conformance suite is observable parity: identical valid atom streams should produce matching volatile state, persistent ledger contents, FSM state, occurrence identities, and canonical execution hash behavior across runtime implementations.

## Formal verification contract

The formal proof layer lowers `.ubldsl` FSM declarations or sequential `.ublasm` program counters into a finite transition system `(S, S0, T)`.

The verification contract covers:

- bounded breadth-first exploration
- witness and counterexample reporting
- reachability checks
- non-terminal deadlock checks
- declared-state preservation
- persistent-schema immutability

SMT-LIB2 output uses integer state identifiers and a pure transition predicate. Lean 4 output declares a finite `UBLState`, decidable equality, reachability, and an exhaustive theorem. Exported proof text is deterministic for identical source.

`solver_verified` is only considered true when an external solver actually runs.

## Important limitation

The formal-verification claim is **bounded to the finite models lowered into the proof system**. It is not a claim of universal correctness for arbitrary programs, hardware, networks, or future extensions.

## Review questions

External reviewers are invited to challenge:

- whether the observable parity definition is sufficiently complete
- whether occurrence identity belongs in the kernel or should remain an overlay
- whether the state space encoded for SMT omits meaningful failure classes
- whether RESET and control precedence introduce hidden edge cases
- whether proof obligations should include stronger liveness or temporal properties
