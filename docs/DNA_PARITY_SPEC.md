# HexDoku DNA / Parity Model v0.2

Status: **Draft / experimental**

This document defines the current concrete model for a HexDoku board that begins with 25 unresolved coordinates.

The core object is **not a Sudoku solving trace**. It is a deterministic 25-stage evaluation-table trajectory.

## 1. Core definitions

### DNA

**DNA** is the canonical sequence of evaluation/probability tables produced while the unresolved region contracts from 25 coordinates to 1.

~~~text
P0: 25 unresolved coordinates
P1: 24 unresolved coordinates
P2: 23 unresolved coordinates
...
P23: 2 unresolved coordinates
P24: 1 unresolved coordinate
~~~

The number of evaluated coordinate states is:

~~~text
25 + 24 + ... + 1 = 325
~~~

If every coordinate evaluates nine candidates and every finalized value is represented by 8 bits, the raw value stream is:

~~~text
325 × 9 × 8 = 23,400 bits = 2,925 bytes
~~~

This 2,925-byte figure is the uncompressed 8-bit candidate-value trajectory only. Metadata and optional terminal-reference bytes are accounted separately.

### Parity

**Parity** is the fully materialized final 9×9, 81-cell table.

Parity is not defined here as a conventional parity bit or an error-correcting-code check symbol. It is the completed reference state against which reconstruction can be verified.

The last cell may contain a canonical symbol, byte sequence, ID, reference, or other typed value. It does not have to be one of the digits 1 through 9.

### Terminal Reference

The final unresolved coordinate is a **Terminal Reference**.

The first 24 state transitions do not need to derive a conventional numeric value for this final cell. The final cell is resolved or checked against the referenced Parity.

~~~text
24 deterministic commits
        |
        v
one unresolved terminal coordinate
        |
        v
Terminal Reference / Parity lookup or verification
        |
        v
complete 81-cell Parity
~~~

## 2. Sudoku rules are not normative

HexDoku may use a Sudoku-shaped 9×9 topology, but standard Sudoku constraints are **not required** by this model.

The protocol does not require:

- row uniqueness;
- column uniqueness;
- 3×3 box uniqueness;
- human Sudoku techniques;
- a conventional Sudoku solving order.

What is required is:

1. a canonical coordinate order;
2. deterministic evaluation tables;
3. deterministic state transitions for the first 24 commits;
4. a unique interpretation of the Terminal Reference;
5. a uniquely verifiable final Parity under the selected rule version.

## 3. Canonical coordinate sequence

At initialization, collect the 25 unresolved coordinates and order them strictly by board position:

~~~text
top row to bottom row
and within each row:
left to right
~~~

For a 9×9 board this is row-major order:

~~~text
r1c1 -> r1c2 -> ... -> r1c9
-> r2c1 -> ... -> r2c9
-> ...
-> r9c1 -> ... -> r9c9
~~~

Let the resulting unresolved-coordinate sequence be:

~~~text
E0, E1, E2, ... E24
~~~

This sequence is fixed for the lifetime of that DNA trajectory.

HR, probability values, execution timing, CPU/GPU scheduling, or Sudoku heuristics do **not** change this coordinate sequence.

## 4. Twenty-five evaluation stages, twenty-four commits

The model distinguishes **evaluation stages** from **commit transitions**.

At stage t:

~~~text
Pt evaluates Et, Et+1, ... E24
~~~

Therefore:

~~~text
P0 -> 25 coordinates
P1 -> 24 coordinates
...
P23 -> 2 coordinates
P24 -> 1 coordinate
~~~

After each of P0 through P23, coordinate Et is committed using the versioned deterministic value resolver.

After P24, E24 is **not required to be committed as a digit**. It is the Terminal Reference.

Thus the trajectory contains:

- 25 evaluation tables;
- 24 deterministic normal commits;
- 1 terminal reference resolution;
- 325 evaluated coordinate states.

This distinction is normative.

## 5. Per-coordinate evaluation table

For each active coordinate c in stage t, the baseline candidate domain is:

~~~text
D = {1,2,3,4,5,6,7,8,9}
~~~

The versioned evaluator computes:

~~~text
Q(t,c) = [
  (1, q1),
  (2, q2),
  ...
  (9, q9)
]
~~~

where q is a deterministic finalized numeric value.

The rule version must pin the evaluation formula, constants, numeric precision, rounding, saturation/clamping, exceptional-value handling, candidate iteration rules, byte order, and bit order.

Same input state plus same rule version must yield bit-identical q values.

## 6. Canonical probability/value ordering

After the nine q values are calculated, entries are canonically ranked by:

~~~text
1. q ascending
2. candidate symbol/digit ascending as the tie-break
~~~

This produces one unique ordered table even when two q values are equal.

If HDC and HDE can both recompute the same permutation, the permutation itself need not be transmitted.

The finalized q bit patterns may be reused directly as immediate values, hash input, table indexes, Seed material, or bus payload material.

## 7. HexDoku Hamming Rank (HR)

HexDoku HR is a project-specific unresolved-multiplicity rank, not standard bitwise Hamming distance.

~~~text
HR = unresolved candidate multiplicity - 1
~~~

Range:

~~~text
HR0 -> one candidate remains / logically determined, possibly not yet committed
HR1 -> two unresolved candidates
...
HR8 -> nine unresolved candidates / maximum multiplicity
~~~

HR describes the state of an evaluated coordinate.

HR does **not** choose the next coordinate. The next normal commit coordinate is already fixed by the initial sequence E0..E23.

If serialized explicitly, HR requires 4 bits. If HDE deterministically recomputes it, those bits may be omitted.

## 8. Deterministic resolver

HexDoku requires a versioned resolver, but it does not require a Sudoku resolver.

For stages P0 through P23:

~~~text
value_t = Resolve(
  rule_version,
  stage=t,
  coordinate=Et,
  current_state,
  evaluation_table=Q(t,Et)
)
~~~

Resolve must be deterministic, total for valid inputs, uniquely tie-broken, versioned, and reproducible across conforming HDC/HDE implementations.

The exact resolver function remains a separately versioned component.

The invariant is:

~~~text
Resolve_HDC(t) == Resolve_HDE(t)
~~~

for every one of the 24 normal commits.

## 9. Terminal stage

P24 contains the final active coordinate E24.

Its evaluation row may still be generated and retained as part of the 25-table DNA trajectory, but it does not have to force a digit 1..9 into the final cell.

Instead:

~~~text
E24 := ResolveTerminal(ParityReference, rule_version)
~~~

The terminal value may be a canonical number, character, byte string, hash/reference fragment, object ID, Seed reference, or typed protocol symbol.

A type/length rule is required so that the representation remains unambiguous.

A hash alone can verify a known Parity but cannot reconstruct unknown Parity content. If the terminal value must be recovered, the referenced Parity or an equivalent deterministic source must be available.

## 10. Canonical DNA serialization

The logical DNA stream is serialized stage-major.

Within each stage, coordinates remain in the fixed E-order.

Within each coordinate, candidate values use the canonical probability/value ordering.

~~~text
DNA =
P0[E0..E24]
||
P1[E1..E24]
||
...
||
P24[E24]
~~~

For 8-bit q values, the baseline q-only stream contains 2,925 bytes.

Coordinates and stage numbers can be implicit because their sequence is known from the initial unresolved-coordinate list.

Derived HR and candidate permutation fields can also be omitted when HDE can recompute them exactly.

## 11. HCT prepass and most-frequent values

HDC may perform a complete prepass over the canonical DNA q stream before emitting the compressed payload.

From the 2,925 q symbols it constructs a versioned **HexDoku Canonical Table (HCT)**:

~~~text
1. count each quantized q value
2. order values by frequency descending
3. break equal-frequency ties by numeric value ascending
4. assign canonical symbol IDs/codes
~~~

The most frequent value is therefore known before the compressed q payload is encoded.

To avoid a decoding circular dependency, one of these must be true:

1. HCT is serialized in a header before the payload; or
2. HCT is deterministically regenerable from shared Seed/rules/state and is therefore omitted.

HDE must know the exact HCT before decoding any HCT-dependent payload.

After HCT is established, HDC may apply canonical entropy coding, prediction, turn-to-turn deltas, repeated-value omission, or residual coding.

Actual compression ratio must be measured from real trajectories.

## 12. HDC procedure

~~~text
input / source state
    |
    v
construct initial board and E0..E24
    |
    v
generate P0..P24 deterministically
    |
    v
canonicalize every Q(t,c)
    |
    v
form DNA q stream
    |
    v
HCT frequency prepass
    |
    v
encode HCT/header if required
    |
    v
encode predictable/repeated values + residuals
    |
    v
emit Seed + rule versions + compressed DNA + Parity reference/check
~~~

HDC is allowed to be computationally expensive.

## 13. HDE procedure

~~~text
Seed + rules + compressed DNA + Parity reference/check
    |
    v
recover/regenerate HCT
    |
    v
decode canonical DNA q stream
    |
    v
recreate P0..P24 in canonical order
    |
    v
perform the same 24 normal commits
    |
    v
resolve terminal E24 from the Parity reference/source
    |
    v
materialize 81-cell Parity
    |
    v
verify final digest/reference
~~~

HDE must fail on ambiguity, missing required state, or verification mismatch.

## 14. Required equality

For every stage and every active coordinate:

~~~text
Q_HDC(t,c) == Q_HDE(t,c)
HR_HDC(t,c) == HR_HDE(t,c)
~~~

For the 24 normal commits:

~~~text
Commit_HDC(t) == Commit_HDE(t)
~~~

And finally:

~~~text
Parity_HDC == Parity_HDE
~~~

All equality above means canonical bit equality.

## 15. Cryptographic mode

The 9×9 topology, coordinate order, format, and algorithm version may be public.

If HexDoku is used in a cryptographic setting, confidentiality must not rely merely on hiding the algorithm or on Sudoku-like complexity.

A cryptographic profile should use standard cryptographic primitives for secret-key derivation, pseudorandom functions, encryption/authentication, or commitments as appropriate.

Security evaluation should measure what remains unresolved after public tables/coordinates are revealed, rather than assuming that board complexity equals security.

HexDoku v0.2 makes **no claim of proven cryptographic security**.

## 16. Information accounting

Benchmarks must separately report:

- raw DNA q bytes;
- compressed DNA bytes;
- HCT/header bytes;
- Seed/key/reference bytes;
- Parity storage or referenced shared state;
- decoder/rule-table storage;
- actual independent source bits represented.

This separation is required for fair compression claims.


## 17. Parity as a permutation/address map

The final Parity may map its canonical cells to block IDs or content hashes.

This allows the DNA trajectory to select a final canonical ordering of a shared block universe.

~~~text
DNA trajectory
   |
   v
final Parity
   |
   v
block-ID / hash permutation
   |
   v
ordered block stream
~~~

The Parity is therefore not limited to representing solved puzzle symbols. It may function as a deterministic ordering/address table.

The mapping from a Parity cell to an ID/hash-table entry is reconstruction-critical and must be versioned.

## 18. Ordering compression boundary

HexDoku may replace an explicit permutation with a shorter descriptor only when the permutation is sufficiently constrained or derivable.

For n distinct arbitrary elements there are n! possible orders.

For 81 elements:

~~~text
log2(81!) ≈ 401.17 bits
~~~

Thus a universal lossless encoding of arbitrary 81-element permutations still requires about 402 fixed bits of distinguishing capacity.

HexDoku gains arise when the selected Parity/order is implied partly by:

- shared Seed/rules;
- the 25-stage DNA trajectory;
- a restricted valid-order family;
- previous state;
- nonuniform probability;
- HCT or other shared tables;
- residual-only transmission.

The block contents themselves remain separate information unless already shared, retrievable, or compressed by another codec.

See [PERMUTATION_ADDRESSING.md](PERMUTATION_ADDRESSING.md).
