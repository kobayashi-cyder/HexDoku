# Order / HR Corpus Benchmark — 500 Completed Sudokus

Status: **Measured reference corpus / experimental**

Date: 2026-09-24

## Configuration

~~~text
profile                 = sudoku-order-bearing-mrv-v0
HDC family              = fixed 9+9+7
candidate masks/board   = 36
completed boards        = 500
total mask evaluations  = 18,000
generator               = randomized exact Sudoku backtracking
RNG seed                = 20260924
target rule             = minimum candidate count, row-major tie-break
value rule              = ascending digit + exact feasibility check
~~~

The benchmark script is `reference/corpus_benchmark.py`.

## Main result

~~~text
boards with >=1 exact-round-trip mask = 367 / 500 = 73.4%
boards with no valid fixed mask       = 133 / 500 = 26.6%
accepted masks                        = 3,780 / 18,000 = 21.0%
~~~

Every accepted mask produced a distinct derived order within its own source board in this corpus, so for every board:

~~~text
K = accepted_mask_count
~~~

for this measured sample.

## Reachable order count K

Across all 500 boards:

| metric | K | log2(K) bits |
|---|---:|---:|
| minimum | 0 | 0 |
| mean | 7.56 | 2.1491 mean log2(K) |
| median | 6 | 2.5850 |
| maximum | 30 | 4.9069 |

Among only the 367 boards with at least one valid mask:

| metric | K | log2(K) bits |
|---|---:|---:|
| minimum | 1 | 0 |
| mean | 10.2997 | 2.9280 mean log2(K) |
| maximum | 30 | 4.9069 |

The hard fixed-family ceiling remains:

~~~text
K <= 36
log2(K) <= log2(36) = 5.169925... bits
~~~

Therefore the current fixed `9+9+7` family cannot carry anything close to the absolute `log2(25!) ≈ 83.68`-bit arbitrary-permutation ceiling.

## Guarantee result

The measured guaranteed order capacity of the current fixed 36-mask family is:

~~~text
0 bits
~~~

for two independent reasons observed in the corpus:

1. 133 boards had `NO_MASK` under the fixed family;
2. some successful boards had only `K=1`, which carries zero independent order choice.

This does not make the deterministic order useless: HDE can still omit a separately transmitted order description when the order is merely derived metadata. It means the current family does not yet guarantee an **information-bearing variable order channel**.

## HR results

Across all 3,780 accepted masks, target-stage HR counts were:

~~~text
HR0 = 86,101
HR1 =  8,399
total target evaluations = 94,500 = 3,780 × 25
~~~

No HR2 target was observed in this 500-board corpus.

Therefore target-only branch-reference slots were:

~~~text
sum(HR_target) per accepted mask:
minimum = 1
mean    = 2.22196
maximum = 7
~~~

Across the full 325-state DNA trajectory:

~~~text
HR0 = 241,908
HR1 = 621,408
HR2 = 365,184
total = 1,228,500 = 3,780 × 325
~~~

Thus:

~~~text
sum(HR_DNA) per accepted mask:
minimum = 258
mean    = 357.61270
maximum = 467
~~~

These are structural alternative-reference slot counts. They are **not** independent payload-bit counts.

## HDE work

Every accepted 25-hole board performed exactly:

~~~text
25 + 24 + ... + 1 = 325
~~~

candidate-cell evaluations under the simple repeated-scan implementation.

Exact feasibility recursion calls ranged from:

~~~text
minimum = 325
mean    = 338.8431
maximum = 673
~~~

These are algorithm-level calls/evaluations, not measured CPU instructions.

## Interpretation

The benchmark separates four different claims:

1. **Metadata omission:** coordinates, deterministic order, HR, and branch-slot positions can be regenerated from the received board when the profile is fixed.
2. **Order capacity:** the number of deliberately selectable derived orders is only `log2(K)` bits.
3. **HR slot structure:** `sum(HR)` counts alternative-reference positions, not independent entropy.
4. **Coverage:** the fixed 36-mask `9+9+7` family fails to produce any exact-round-trip board for 26.6% of this corpus.

## Consequence for the next HDC step

The next encoder improvement should target **coverage first**, then order capacity.

A larger HDC family should aim to:

- eliminate `NO_MASK` cases;
- guarantee at least two valid masks where possible (`K>=2` gives at least one order bit);
- increase minimum K, not only average K;
- retain low HDE reconstruction cost;
- measure whether more masks merely duplicate the same derived order;
- keep all extra selector/context bytes in compression accounting.

The already-documented generalized `9+9+7` family has 9,072 configurations and is a natural next experiment, but no performance claim is made until it is benchmarked.

## Scope warning

This is a finite 500-board corpus. It is substantially stronger evidence than the earlier single-Parity sample, but it is not a proof over all completed Sudoku grids.