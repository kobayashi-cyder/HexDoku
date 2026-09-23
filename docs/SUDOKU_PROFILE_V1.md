# HexDoku Sudoku Profile v1

Status: **Reference baseline / experimental**

This document defines the first reference rule profile for HexDoku.

HexDoku Core remains capable of future non-Sudoku rule profiles, but **the first implementation and benchmark profile uses ordinary 9×9 Sudoku constraints** so that the probability/evaluation trajectory has a simple, auditable baseline.

## 1. Purpose

The purpose of Sudoku Profile v1 is not to claim that HexDoku must always be Sudoku.

It provides a fixed baseline for measuring:

- deterministic 25-stage table generation;
- HDC/HDE bit equality;
- Hamming Rank behavior;
- HCT/entropy statistics;
- trajectory compression;
- reconstruction cost;
- later improvement from future Payload Profiles.

Any future payload-specific rule must be compared against this baseline rather than silently changing the v1 rules.

## 2. Board rules

Sudoku Profile v1 uses:

~~~text
board: 9 × 9
symbols: 1..9
row constraint: no duplicate digit
column constraint: no duplicate digit
3 × 3 box constraint: no duplicate digit
~~~

The starting board must have at least one valid Sudoku completion.

For tests that require a single known Parity, a unique-solution starting board SHOULD be used.

## 3. Initial unresolved coordinates

The reference profile uses 25 unresolved coordinates.

They are collected once from the starting board and sorted row-major:

~~~text
E0, E1, ... E24
~~~

The schedule never changes.

At stage t, active unresolved coordinates are:

~~~text
Et, Et+1, ... E24
~~~

HR or probability values do not choose the next coordinate.

## 4. Sudoku candidate set

For an active coordinate c, let:

~~~text
Candidates(c) = {1..9}
                - digits already used in c's row
                - digits already used in c's column
                - digits already used in c's 3×3 box
~~~

This local candidate set is deterministic.

HexDoku Hamming Rank is:

~~~text
HR(c) = |Candidates(c)| - 1
~~~

so HR0 means one locally legal Sudoku candidate remains and HR8 means all nine symbols remain locally possible.

## 5. Fast deterministic q-distribution

Sudoku Profile v1 defines an inexpensive local distribution so q tables can be generated immediately without floating-point behavior.

For each active coordinate c and candidate digit d:

1. if d is not in Candidates(c), raw(c,d) = 0;
2. otherwise collect the unique unresolved Sudoku peers of c: cells sharing its row, column, or box;
3. let peer_count(c,d) be the number of those peers whose local candidate set also contains d;
4. define raw(c,d) = 21 - peer_count(c,d).

A standard Sudoku cell has at most 20 unique peers, so an allowed digit receives an integer raw score from 1 through 21.

Convert the nine raw scores to eight-bit q values using integer-only normalization:

~~~text
S = sum(raw(c,1)..raw(c,9))
base_d = floor(raw(c,d) * 255 / S)
~~~

Any remainder needed to make the q sum exactly 255 is distributed by largest fractional remainder, with digit ascending as the final tie-break.

Forbidden candidates remain q=0.

Therefore:

~~~text
sum(q1..q9) = 255
q_d in 0..255
~~~

and the result is bit-identical across conforming implementations.

No floating-point arithmetic is required.

## 6. Canonical q ordering

Calculation is performed in digit identity order 1..9.

For ranked/canonical table views, entries are sorted by:

~~~text
q ascending
then digit ascending
~~~

The identity-order q1..q9 vector remains available for fixed-width packing.

## 7. Commit resolver

For stages P0 through P23, the scheduled target is Et.

The resolver examines locally legal candidates in:

~~~text
q descending
then digit ascending
~~~

and selects the first candidate for which the resulting board still has at least one complete valid Sudoku solution.

The feasibility test is exact and deterministic; a reference backtracking solver is sufficient.

If no candidate preserves a valid completion, the profile fails rather than guessing.

This gives a deterministic valid Sudoku path while keeping q generation itself inexpensive.

## 8. Twenty-five evaluation tables

~~~text
P0  : 25 active coordinates
P1  : 24
...
P23 : 2
P24 : 1
~~~

The trajectory therefore contains:

~~~text
25 + 24 + ... + 1 = 325 evaluated coordinate states
~~~

With nine 8-bit q values per state:

~~~text
325 × 9 × 8 = 23,400 bits = 2,925 bytes
~~~

before HCT, delta, prediction, or entropy coding.

## 9. Parity

For Sudoku Profile v1, **ParityGrid** is the completed valid 81-digit Sudoku solution.

This is the baseline reference object used to verify reconstruction.

At P24, the final Sudoku digit is not treated as a free payload symbol. It is obtained/verified from the Sudoku solution state.

## 10. Terminal word in Sudoku v1

The final q vector can still be packed as:

~~~text
Q72 = Encode8(q1)||...||Encode8(q9)
~~~

and a 4-bit terminal extension field may exist structurally:

~~~text
T76 = Q72 || ext4
~~~

However, in **Sudoku Profile v1**:

- Q72 is derived from Sudoku state and is not free payload;
- ext4 is reserved and MUST be 0000;
- T76 MUST NOT be advertised as 76 bits of independent payload or selector entropy.

In a normal final-one-cell Sudoku state, the q distribution is expected to be highly constrained and typically collapses to one legal candidate.

Therefore the previously discussed 2^76 permutation-selector capacity belongs to a **future Payload Profile**, not to the Sudoku v1 baseline.

## 11. Future Payload Profile boundary

A later profile may redefine how terminal payload is carried.

Possible future mechanisms include:

- a separate payload sidecar;
- a payload-specific terminal word;
- a different candidate alphabet;
- a keyed selector;
- a permutation/address profile;
- a larger multi-cell payload channel.

Those mechanisms must use a new profile/version and must not change Sudoku Profile v1 results.

Conceptually:

~~~text
HexDoku Core
├─ Sudoku Profile v1       <- first reference implementation
│  ├─ classic Sudoku constraints
│  ├─ 25-stage q tables
│  ├─ deterministic commits
│  └─ valid Sudoku ParityGrid
│
└─ Payload Profile vN      <- future work
   ├─ block/hash ordering
   ├─ terminal payload
   ├─ custom selector rules
   └─ alternative resolver/domain
~~~

## 12. Benchmark order

The first measurements SHOULD be:

1. generate many valid 25-unresolved Sudoku boards;
2. compute all 325 q vectors;
3. verify HDC/HDE table equality;
4. measure q-value histograms and entropy;
5. measure turn-to-turn q reuse;
6. measure HCT compression;
7. measure full 2,925-byte trajectory compression;
8. only after the baseline is stable, test a Payload Profile.

This keeps Sudoku-derived compression effects separate from later payload-specific engineering.
## 13. HDC-Lite 9+9+7 baseline

The first encoder profile paired with Sudoku Profile v1 is `hdc-lite-9-9-7-v1`.

Starting from a completed ParityGrid:

~~~text
digit 1: 9 holes
digit 2: 9 holes
digit 3: 7 holes
total: 25 holes
~~~

The nine positions containing digit 3 are sorted row-major. The encoder chooses which two remain visible.

Therefore only 36 hole masks exist and a six-bit rank is sufficient.

HDC MUST test candidate masks by running the same HDE reconstruction rules without using the hidden ParityGrid to select digits. A mask is valid only when the HDE result exactly equals the source ParityGrid.

See [HDC_LITE_V1.md](HDC_LITE_V1.md) for the canonical scoring and generalized 9+9+7 mode.

## 14. Minimal packet profile

The current one-board experiment may use a shared canonical solved Sudoku plus a fixed-width 41-bit transform Seed.

HDE reconstructs the completed Parity by deterministic digit/row/band/column/stack permutations and optional transpose.

This path requires no Sudoku-wide rank/unrank and no transmission of q tables.

If a coordinate-bearing channel is enabled and at least 32 reconstructible masks are available, add five payload bits for a 46-bit one-board descriptor.

The transform-Seed profile is restricted to one canonical-grid orbit and is therefore not a universal representation of all Sudoku solutions.
