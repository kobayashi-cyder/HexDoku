# HDE Minimum Packet Profile

Status: **Draft / one-board Sudoku baseline**

This document compares packet size against HDE implementation complexity for exactly one 9×9 Sudoku board.

## 1. Scope

The current scope is intentionally limited to:

~~~text
one received 9×9 Sudoku board
exactly 25 holes
Sudoku Profile v1
one HDE reconstruction
~~~

No multi-board chaining is included.

## 2. Important distinction

The current reference transport is the **received-board profile**: HDE receives the 81-cell board itself. Alternative Seed/rank transports remain research comparisons and are not the current baseline.

HexDoku therefore distinguishes the actual received board from optional alternate encodings of that board.

## 3. Packet-size spectrum

### A. Full Parity direct

Send all 81 Sudoku digits with a simple four-bit representation:

~~~text
81 × 4 = 324 bits = 40.5 bytes
~~~

HDE complexity: trivial. It only validates or consumes the board.

This is the heaviest reference packet in this one-board comparison, but also the simplest decoder.

### B. Direct masked-board packet

Under fixed 9+9+7, visible states are:

~~~text
hole, 3, 4, 5, 6, 7, 8, 9
~~~

which is eight symbols and therefore three bits per cell:

~~~text
81 × 3 = 243 bits = 30.375 bytes
~~~

HDE complexity: very small. It rebuilds row/column/box masks and fills the 25 holes.

Relative to the 324-bit full-grid baseline:

~~~text
reduction = 25.00%
~~~

### C. Arbitrary-Sudoku rank

The known number of completed 9×9 Sudoku solution grids is approximately 6.67 × 10^21, requiring about 72.5 bits to distinguish all grids; a fixed-width representation therefore needs 73 bits.

~~~text
~73 bits = 9.125 bytes
~~~

This is information-efficient for the complete valid-Sudoku set, but it requires a practical canonical rank/unrank algorithm over that entire solution set.

HDE complexity: high compared with the other profiles. This is not the current recommended baseline.

### D. Alternate research transport: canonical Parity + transform Seed

Choose one shared canonical solved Sudoku board and allow only standard Sudoku-preserving transformations:

~~~text
digit relabeling:       9!
row permutations:       6^3
band permutation:       6
column permutations:    6^3
stack permutation:      6
transpose:              2
~~~

The raw transform-parameter space is:

~~~text
9! × 6^8 × 2
~~~

whose binary width is about 40.15 bits, so a fixed 41-bit Seed is sufficient to describe every transform tuple.

~~~text
41 bits = 5.125 bytes
~~~

HDE complexity: low to moderate. It does not solve or enumerate Sudoku. It starts from the shared canonical grid and applies fixed permutations.

Important: this profile covers only the orbit generated from the chosen canonical board under those transformations. It does **not** represent every possible completed Sudoku grid.

### E. Alternate research transport: canonical Seed + coordinate-bearing mode

If the one-board HDC-Lite mask family has at least 32 reconstructible masks, five fixed payload bits can be assigned to 32 masks:

~~~text
41-bit Parity transform Seed
+ 5-bit coordinate payload
= 46 bits = 5.75 bytes
~~~

The remaining reconstructible masks, if any, may be reserved.

HDE complexity remains low to moderate.

### F. Parity already shared

If the exact Parity is already known to both endpoints, it does not need to be transmitted again.

~~~text
Neutral mode:             0 new Parity bits
Coordinate-bearing mode: up to 5 payload bits if >=32 valid masks
~~~

This is a shared-state synchronization case, not a self-contained encoding of an unknown Sudoku board.

## 4. Heaviest versus lightest self-contained result

For the currently discussed self-contained one-board profiles:

~~~text
heaviest simple baseline: full Parity direct = 324 bits
lightest restricted profile: canonical transform Seed = 41 bits
~~~

Difference:

~~~text
324 - 41 = 283 bits
41 / 324 ≈ 12.65%
reduction ≈ 87.35%
size ratio ≈ 7.90 : 1
~~~

If the comparison starts from the already-masked 243-bit board:

~~~text
243 -> 41 bits
reduction ≈ 83.13%
size ratio ≈ 5.93 : 1
~~~

These are representation-size comparisons, not measured general-purpose compression results.

## 5. Simplicity spectrum

| Profile | Packet | HDE search | HDE implementation | Coverage |
|---|---:|---|---|---|
| Full Parity direct | 324 bit | none | trivial | any transmitted board |
| Masked board | 243 bit | small Sudoku reconstruction | very small | 9+9+7 boards |
| Arbitrary-Sudoku rank | 73 bit | no Sudoku solve after unrank, but unrank is complex | high | all valid completed Sudoku grids if a complete rank/unrank is implemented |
| Canonical transform Seed | 41 bit | none | low/moderate | one canonical-grid orbit |
| Seed + coordinate payload | 46 bit | none for Parity generation; small mask reconstruction if used | low/moderate | one orbit + coordinate channel |
| Shared exact Parity | 0 Parity bit | none | trivial | only already-shared state |

## 6. Current reference input

The current HexDoku experiment receives the 25-hole board itself.

For a generic Sudoku board, a simple fixed-width representation is 324 bits (`81 × 4`). Under the fixed `9+9+7` profile, the eight visible cell states fit in 243 bits (`81 × 3`).

No separate coordinate list is transmitted because the 25 hole positions are already present in the 81-cell array. No separate solution-value, solve-order, HR, or HR-slot-position fields are transmitted when HDE can regenerate them exactly.

The 41-bit transform Seed remains an alternate restricted transport experiment, not the current received-board baseline.

## 7. Minimal HDE work

For the current received-board profile:

~~~text
read 81-cell board
-> scan once to find 25 holes and build row/column/box masks
-> evaluate candidates with 9-bit masks
-> reconstruct the 25 values under the pinned deterministic rule
-> record the deterministic solve/commit order
-> regenerate HR and branch-slot positions
-> verify final board
~~~

For a no-backtracking path, a simple repeated scan evaluates at most `25+24+...+1 = 325` remaining-cell states. The intended cost is therefore a few thousand simple integer/bit operations, not a measured CPU-instruction guarantee.

## 8. What must still be measured

Benchmark the received-board path directly:

- actual board bytes on wire;
- actual HDE code size and working memory;
- candidate-cell evaluation count;
- measured CPU instructions/cycles;
- number K of distinct solve orders HDC can deliberately realize;
- `log2(K)` order-channel capacity;
- HR histogram and `sum(HR)`;
- reference-dictionary/manifest overhead;
- exact final Parity equality.

Alternate 41-bit transform-Seed experiments must be reported separately.


See [ONE_BOARD_DERIVED_INFORMATION.md](ONE_BOARD_DERIVED_INFORMATION.md) for the authoritative current information accounting.
