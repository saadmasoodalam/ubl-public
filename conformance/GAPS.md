# Public contract gaps recorded during v11

The tests intentionally refuse to invent normative rules not present in [`KERNEL-CONTRACT.md`](../KERNEL-CONTRACT.md).

| Question | Publicly specified | What this reference does |
| --- | --- | --- |
| `PATCH_HEADER` (`payload 0x7D`) | Decoded as control before M routing | Records it as a control; does not assert an unspecified patch operation or framing transition |
| Invalid `START`/`END`/`SYNC` sequences | Controls exist, framing model is named | Records controls; does not claim a particular corruption/recovery FSM |
| Escape literal | Reserved data must be preceded by `ESC` | The immediately following payload is treated as data; dangling `ESC` remains pending |
| EventID initial value `E_0` | Recurrence formula given, seed unspecified | Requires an explicit 32-byte seed; CLI uses a labeled zero-seed illustration |
| Occurrence index | `uint64_be(n)` in recurrence | Numbering starts at 1 in this demonstration; confirm canonical index conventions before comparing outside runtimes |
| Reset volatile value | Clears volatile state | Uses `None` as a symbolic cleared/unset state, not a numeric electrical value |
| Canonical execution hash | Equality required | No algorithm or serialization defined; **not implemented** |
| Semantic ledger head | Must change only on committed entries | Appended ledger entries are observable; **no unstated ledger-head digest** is calculated |
| Invalid/oversized transport frames | Not fully described | No error recovery or transport framing is modeled |

**Specific concern for reviewers:** Is `PATCH_HEADER` a first-class non-data control at the frozen kernel level, or an extension? The public v1.0 document currently includes it in both the control-precedence clause and the frozen control payload list; clarifying its action would make independent runtime parity substantially easier.

This document is a list of verification boundaries, not a rewrite of the frozen contract.
