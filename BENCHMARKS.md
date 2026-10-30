# UBL v1.0 Published Wire-Density Benchmark

The UBL Kernel v1.0.0 release published the following **4-event workload** wire-size comparison.

| Protocol / Format | Wire Bytes | Bytes / Event | Overhead vs UBL |
| --- | ---: | ---: | ---: |
| **UBL 8-bit Atom Stream** | **4 B** | **1.00 B** | **1.00x** |
| **Packed C Bitfield Struct** | **4 B** | **1.00 B** | **1.00x** |
| **TLV Binary Event Log** | **16 B** | **4.00 B** | **4.00x** |
| **Protobuf Varint Frame** | **24 B** | **6.00 B** | **6.00x** |
| **Canonical JSON Event** | **189 B** | **47.25 B** | **47.25x** |

## What this result means

For this specific workload, UBL carries one event per byte and therefore adds no extra per-event wire-framing bytes beyond the 8-bit atom itself. The packed C bitfield baseline has the same density.

## What this result does **not** mean

This benchmark does not establish that UBL is universally more compact than all binary formats for every schema, workload, transport, or compression regime. It does not measure CPU cost, hashing cost, storage-engine cost, network reliability overhead, or application-level metadata.

The comparison is deliberately narrow: **raw wire bytes for the published 4-event semantic workload**.

## Review requested

Useful criticism includes:

- whether the compared representations encode truly equivalent semantics
- whether tags, lengths, field names, framing, or schema assumptions are unfairly distributed
- whether a larger or more heterogeneous workload changes the conclusion
- whether compressed JSON / Protobuf or alternate binary encodings should be added
- whether computational and energy cost should be reported alongside wire density
