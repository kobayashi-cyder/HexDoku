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

## 9. Terminal stage and 76-bit selector

P24 contains the final active coordinate E24.

The 25th probability/evaluation row remains meaningful. Under the baseline 8-bit-q terminal profile, pack the nine finalized q values in fixed candidate identity order:

~~~text
Q76_base =
Encode8(q1) || Encode8(q2) || ... || Encode8(q9)
~~~

This contributes:

~~~text
9 × 8 = 72 bits
~~~

P24 then adds a terminal-only 4-bit field:

~~~text
TerminalExtension4 = 0..15
~~~

The resulting terminal word is:

~~~text
T76 = Q76_base || TerminalExtension4
width(T76) = 76 bits
~~~

The 4-bit TerminalExtension4 is **not HexDoku HR**. HR remains an optional derived state quantity with semantic range 0..8. Reusing an HR nibble would restrict the reachable terminal state count and would not provide a full 76-bit selector field.

The terminal coordinate is therefore not required to force a digit 1..9 into the final cell. Instead, T76 may serve as a typed terminal payload or a selector into a versioned Parity/permutation family.

Nominal field capacity:

~~~text
2^76 = 75,557,863,725,914,323,419,136 selector values
~~~

This is representation capacity. Actual reachable entropy may be lower if the evaluator cannot produce all possible 72-bit q combinations.

A profile claiming the full 76-bit selector domain must specify how every T76 value can be produced or supplied.

### 9.1 Canonical 13-symbol text form

A fixed 76-bit integer can be displayed in 13 symbols using the Base64url alphabet as a radix-64 digit alphabet:

~~~text
13 radix-64 symbols = 78 container bits
76 payload bits
2 high-order states are constrained
~~~

Canonical rule:

- interpret T76 as an unsigned 76-bit big-endian integer;
- encode it as exactly 13 radix-64 digits;
- use the Base64url alphabet `A-Z a-z 0-9 - _`;
- the first digit is restricted to indices 0..15.

This is **not standard byte-oriented Base64url encoding**.

If an implementation instead stores T76 in a 10-byte container and uses standard unpadded Base64url, four container bits must be canonicalized and the text requires 14 characters.

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
HR_HDC(t,c) == HR_HDE(t,c) for HR-bearing states
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


## 19. T76 permutation selection

For a shared block universe U with n distinct blocks, T76 may be interpreted as an integer:

~~~text
s = UInt76(T76)
0 <= s < 2^76
~~~

When n! >= 2^76, a versioned permutation profile can map every selector to a distinct permutation.

One simple normative construction for experimentation is:

~~~text
N      = n!
offset = ContextRank(rule_version, Seed, DNA_prefix, universe_id) mod N
rank   = (offset + s) mod N
Pi     = FactoradicUnrank(n, rank)
~~~

For fixed context, this mapping is injective in s whenever 2^76 <= n!.

For n=81:

~~~text
log2(81!) ≈ 401.17
81! >> 2^76
~~~

so all 2^76 T76 selector values can map to distinct 81-element permutations.

T76 selects a **2^76-sized subset/contextual window** of the complete 81! permutation space. It does not by itself encode all possible 81-element orders.

ContextRank must be deterministic and versioned. If a cryptographic keyed profile is used, its PRF/hash construction must be specified separately.

## 20. Security interpretation of T76

T76 is primarily a selector/address field.

If all 2^76 values are uniformly secret, exhaustive selector search has at most a 76-bit search space. That is below the 128-bit security level normally targeted by modern cryptographic systems.

Therefore T76 should not be advertised as a standalone modern encryption key.

For confidentiality/authentication, use a standard cryptographic construction and treat T76 as a selector, nonce/reference component, truncated tag only where appropriate, or one part of a larger keyed state.

## 21. T76 compression accounting

The terminal selector is a 76-bit state identifier.

For a profile exposing all 2^76 selector states, 76 bits is the minimum uniform lossless selector width.

The apparent compression gain comes from replacing a larger explicit ordering representation with this shared-context selector.

For a 25-element example:

~~~text
naive 5-bit ID list: 25 × 5 = 125 bits
T76 selector:                  76 bits
reduction:                     39.20%
~~~

If the receiver already has the same ID/hash universe, wider explicit identifier lists give larger order-description reductions:

~~~text
25 × 32-bit IDs  -> 90.50% reduction
25 × 64-bit IDs  -> 95.25% reduction
25 × 256-bit IDs -> 98.81% reduction
~~~

These figures exclude any context that is already shared by assumption.

The full descriptor size must add every non-shared Seed, rule identifier, universe/manifest reference, residual, and verification field.

## 22. Full 25! space versus T76 family

A complete arbitrary 25-element permutation requires:

~~~text
log2(25!) ≈ 83.68 bits
~~~

and therefore 84 fixed bits if every order must be supported.

T76 supports at most 2^76 of those orders.

Consequently, T76 is a compact selector for a **restricted/contextual permutation family**, not a universal 76-bit encoding of all 25-element permutations.

## 23. Baseline rule profile

The DNA/Parity Core is profile-independent, but the first reference profile is **Sudoku Profile v1**.

Under that profile:

- symbols are 1..9;
- candidate legality comes from standard Sudoku row/column/3×3 constraints;
- HR is derived from the local Sudoku candidate count;
- q values are generated by the deterministic integer rule defined in `SUDOKU_PROFILE_V1.md`;
- P0..P23 commits must preserve at least one valid Sudoku completion;
- ParityGrid is a completed valid Sudoku board.

## 24. T76 status under Sudoku Profile v1

The generic model can describe `T76 = Q72 || ext4`, but Sudoku Profile v1 does **not** treat this as 76 free payload bits.

~~~text
Q72  = derived from Sudoku probability/evaluation state
ext4 = 0000 (reserved in v1)
~~~

Therefore the effective independent payload capacity of T76 in Sudoku Profile v1 is zero.

A later Payload Profile may define an independent selector, sidecar, alternate q semantics, or other payload carrier. Such a profile must use a new version and must not retroactively change Sudoku Profile v1 trajectories.

See [SUDOKU_PROFILE_V1.md](SUDOKU_PROFILE_V1.md).

## 25. HR-derived branch-reference slots

HexDoku may use HR as a structural count of alternative candidate branches.

~~~text
HR = candidate_count - 1
~~~

If one canonical candidate is treated as an implicit anchor, an HR value `h` exposes exactly `h` alternative branch-reference slots.

Examples:

~~~text
HR0 -> 0 alternative slots
HR1 -> 1
HR2 -> 2
...
HR8 -> 8
~~~

A slot may map to a hash, object/chunk ID, manifest index, Seed reference, or a dictionary index under a separately versioned profile.

Hashes remain identifiers/checks; unknown content is not reconstructed from a digest alone.

Two accounting scopes are defined:

~~~text
B_target = sum_t HR(t,E_t)
B_DNA    = sum_t sum_{c in active(t)} HR(t,c)
~~~

With 325 evaluated coordinate states and generic HR<=8:

~~~text
B_DNA <= 2,600 slots
~~~

For a `9+9+7` trajectory whose legal candidate domain remains within `{1,2,3}`, HR<=2 and:

~~~text
B_DNA <= 650 slots
~~~

These bounds count structural positions only.

If K complete branch/reference assignments are actually reachable while preserving valid deterministic reconstruction and exact Parity, independent channel capacity is at most:

~~~text
log2(K) bits
~~~

not `slot_count × reference_width` by default.

HDE may omit explicit HR and branch-position metadata when the received board and pinned rule profile regenerate them exactly.

See [HR_BRANCH_REFERENCES.md](HR_BRANCH_REFERENCES.md).
