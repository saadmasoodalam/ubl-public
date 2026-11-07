# UBL Hardware Validation v4 — Public Results Summary

**Architect:** Saad Masood  
**Status:** Experimental FPGA toolchain evaluation; **not** a physical silicon result  
**Benchmark date:** November 8, 2026 (Pakistan Standard Time)  
**Frozen semantic baseline:** UBL Kernel v1.0  
**Toolchain:** Icarus Verilog, Yosys, nextpnr-ice40  
**FPGA target for tool-based routing:** Lattice iCE40 HX8K, CT256 package, seed 1

## What was tested

UBL's 8-bit atom comprises a seven-bit payload and rightmost Bit-0 routing
indicator: 0 routes permitted data to transient state, and 1 routes permitted
data to an append-only semantic ledger. Control precedence and RESET semantics
remain part of the frozen contract. A separate readback-enabled *experimental*
hardware design was used so ledger contents would remain observable to
FPGA synthesis. The original RTL was not modified for this experiment.

The private GitHub Actions workflow completed successfully in run
`42418495429` on November 8, 2026 PKT. The implementation, complete RTL,
private test vectors, and detailed automation remain undisclosed.

## Verified tool-reported results

| Check or measurement | Result |
| --- | --- |
| Strict v2 RTL validation | 64/64 checks |
| v3 directed pairwise/triple tests | 108/108 checks |
| Experiment/frozen-RTL equivalence scenarios | 171/171 checks |
| Total checks across suites | 343/343; some conditions overlap |
| Input stimulus: mixed/control framed | 512/512 atoms accepted |
| Input stimulus: persistent writes | 512/512 atoms accepted |
| Input initiation interval in those RTL simulations | 1 clock per atom |
| Synchronous ledger read latency in experimental design | 1 clock edge |
| Experimental readable ledger: mapped LUT4 | 71 |
| Experimental readable ledger: mapped flip-flops | 49 |
| Experimental readable ledger: mapped carry primitives | 8 |
| Experimental readable ledger: mapped iCE40 Block RAM | 2 |
| Experimental readable ledger: total mapped primitive instances | 130 |
| Original write-only top: estimated routed Fmax | 177.78 MHz |
| Readback-enabled experiment: estimated routed Fmax | **188.08 MHz** |
| Idealized theoretical input rate for experimental design | **188.08 million U-Atoms/second** |

The throughput figure is obtained from the experimental design's
nextpnr-estimated Fmax together with the observed 1-atom-per-cycle input
initiation interval. It is **not** a measured FPGA throughput.

## Explicit limitations

- No physical FPGA board was programmed or operated in these results.
- Placement/routing used automatically selected, unconstrained I/O locations,
  not board-specific electrical, pin, or timing constraints.
- Clock speed is a nextpnr tool estimate for one selected device/package and
  routing seed; it is not a guaranteed operating clock or silicon timing signoff.
- The input stream is continuously supplied without ready/backpressure; this
  does not measure real-world transport, commit acknowledgment, or source stalls.
- The ledger read port exists in the *experimental* design, not the frozen
  public top-level interface. The original top's write-only memory may be
  eliminated by synthesis and therefore is not a fair physical-cost comparator.
- Ordinary FPGA Block RAM is volatile at power loss. Nonvolatile persistence,
  power-fail commits, and recovery have not been physically demonstrated.
- SHA-256 execution EventID chaining is not included in these reported
  on-chip RTL resource or timing measurements.
- No fair, functionally equivalent conventional-controller baseline has yet
  been built or compared. These numbers do not establish superior power,
  performance, area, or universal language efficiency.
- The three validation suites contain overlapping tests; 343 is the sum of
  their check counts, not 343 independent proof obligations.
- This is bounded functional testing, not exhaustive formal proof.

## Next checks before stronger claims

1. Construct an independently designed conventional implementation with the
   same input semantics, memory depth, reset behavior, readback observability,
   and control handling.
2. Compare mapping, routed Fmax, cycle latency, and resource use under
   identical constraints on the same FPGA.
3. Perform actual physical FPGA experiments, including I/O, timing,
   reset/power-loss behavior and durability architecture.

## Project references

- [Public kernel contract](KERNEL-CONTRACT.md)
- [Current public disclosure boundary](DISCLOSURE.md)
- [Public review questions](REVIEW.md)
- [Public research whitepaper](https://dadastore.co/research/papers/ubl-kernel-v1.html)
- [Archived v1.0 public-review baseline](https://doi.org/10.5281/zenodo.23845298)

This v4 update is a *supplemental engineering report*, not a replacement of
the archived v1.0 public-review release or a disclosure of the private codebase.
