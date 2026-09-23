# Order-Bearing Sudoku Profile v0

Status: **Experimental research profile**

This profile is separate from the fixed-order `sudoku-v1` baseline.

## 1. Why a separate profile is required

The baseline Sudoku Profile v1 fixes the unresolved-coordinate schedule once:

~~~text
E0, E1, ... E24 = row-major hole order
~~~

and HR/q never reorder it.

Therefore, relative to the fixed E identities, baseline `sudoku-v1` has:

~~~text
K_order = 1
order capacity = log2(1) = 0 bits
~~~

A variable solve order cannot be claimed from that profile.

To study order as an information-bearing derived structure, HexDoku defines this separate experimental profile.

## 2. Received object

HDE receives one 9×9 board with exactly 25 holes.

No separate order field is received.

## 3. Dynamic target rule

At every step:

1. compute the legal Sudoku candidate set for every unresolved coordinate;
2. choose the coordinate with the smallest candidate count (minimum HR);
3. break equal candidate-count ties by row-major coordinate;
4. resolve the chosen digit deterministically;
5. commit it and repeat.

Thus the target coordinate is a deterministic function of the current board state.

Equivalent target key:

~~~text
(candidate_count, row, column)
~~~

ascending lexicographically.

## 4. Value resolver

For the selected coordinate, consider candidate digits in ascending numeric order.

Choose the first candidate for which at least one complete valid Sudoku solution remains.

The feasibility check is exact and deterministic.

If no candidate preserves a completion, reconstruction fails.

## 5. Derived order

The resulting sequence of 25 coordinates is:

~~~text
O(B) = [c0, c1, ... c24]
~~~

where B is the received 25-hole board.

No standalone 84-bit permutation rank is transmitted.

Across an allowed HDC board family F, define:

~~~text
K = | { O(B) : B in F and HDE(B) == source Parity } |
~~~

The actual independent order-channel capacity of that family is:

~~~text
log2(K) bits
~~~

not `log2(25!)` unless all 25! orders are actually reachable.

## 6. Fixed 9+9+7 HDC family

For one fixed completed ParityGrid, the current HDC-Lite family has only 36 masks:

~~~text
remove all 1s
remove all 2s
remove seven 3s
choose the two visible 3 positions
C(9,2) = 36
~~~

Therefore, for one fixed ParityGrid under this HDC family:

~~~text
K <= 36
log2(K) <= log2(36) = 5.169925... bits
~~~

This is a much tighter bound than 83.68 bits.

To approach the full 25! order space, HDC would need a much larger board-construction family with at least 25! distinguishable valid received boards/order outcomes.

## 7. HR reference slots

The dynamic profile also regenerates HR at every evaluated state.

With one implicit anchor candidate:

~~~text
alternative reference slots = HR
~~~

The slot positions are derived from the board and do not need separate position metadata.

The reference values themselves still need to be transmitted/shared/retrievable.

## 8. Benchmark metrics

For every ParityGrid and HDC family report:

- candidate masks/boards tested;
- boards accepted by exact round trip;
- K distinct derived orders;
- `log2(K)`;
- target HR histogram;
- full-DNA HR histogram;
- `sum_hr_targets`;
- `sum_hr_dna`;
- candidate-cell evaluations;
- feasibility-search calls;
- reconstruction time;
- exact source-Parity equality.

## 9. Reference sample

The repository reference benchmark includes one canonical solved Sudoku and enumerates all 36 fixed `9+9+7` masks.

Those results are a **single-board sample**, not a general HexDoku performance claim.
## 10. Current single-Parity reference result

The reference implementation in `reference/one_board_benchmark.py` was evaluated against its one built-in canonical solved Sudoku.

For the 36 fixed `9+9+7` masks:

~~~text
masks tested                 = 36
exact round-trip accepted    = 27
rejected                     = 9
distinct derived orders K    = 27
log2(K)                      = 4.754887502... bits
family theoretical maximum   = log2(36) = 5.169925001... bits
candidate-cell evaluations   = 325 per accepted board
sum_hr_targets range         = 1..3
sum_hr_dna range             = 331..418
~~~

Aggregate target HR observations across the 27 accepted boards:

~~~text
HR0 = 628
HR1 = 47
~~~

Aggregate full-DNA HR observations across the same boards:

~~~text
HR0 = 2,151
HR1 = 3,185
HR2 = 3,439
~~~

This is a single canonical-Parity sample only. It demonstrates that the dynamic profile can produce multiple derived orders, but it does not establish a guaranteed minimum K or general compression ratio.
